
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
import os
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import sys
# ------------------------- 
# Utilitaires / Chargement
# -------------------------
def load_excel_sheets(xlsx_path: str) -> Dict[str, pd.DataFrame]:
    """Charge les feuilles attendues (si elles existent) et renvoie un dict."""
    xlsx = pd.ExcelFile(xlsx_path)
    expected = ['personne_morale', 'personne_physique', 'Contrats', 'sinistres', 'Mapping_Produits']
    sheets = {}
    for name in expected:
        if name in xlsx.sheet_names:
            sheets[name] = pd.read_excel(xlsx, sheet_name=name)
        else:
            sheets[name] = pd.DataFrame()
    return sheets

def safe_to_datetime(s: pd.Series, errors='coerce') -> pd.Series:
    return pd.to_datetime(s, errors=errors)

def clean_nan_values(value):
    """Nettoie les valeurs NaN et les remplace par des valeurs appropriées."""
    if pd.isna(value):
        return None
    elif isinstance(value, str) and value.lower() in ['nan', 'null', '']:
        return None
    return value

# ------------------------- 
# Classe principale
# -------------------------
class ClientDataExtractor:
    def __init__(self,
                 personnes_physiques: pd.DataFrame,
                 personnes_morales: pd.DataFrame,
                 contrats: pd.DataFrame,
                 sinistres: pd.DataFrame,
                 mapping_produits: pd.DataFrame):
        # Keep copies
        self.pp = personnes_physiques.copy() if not personnes_physiques.empty else pd.DataFrame()
        self.pm = personnes_morales.copy() if not personnes_morales.empty else pd.DataFrame()
        self.contrats = contrats.copy() if not contrats.empty else pd.DataFrame()
        self.sinistres = sinistres.copy() if not sinistres.empty else pd.DataFrame()
        self.mapping = mapping_produits.copy() if not mapping_produits.empty else pd.DataFrame()

        # Normalisations de base : enlever espaces dans les noms de colonnes
        for df in [self.pp, self.pm, self.contrats, self.sinistres, self.mapping]:
            if not df.empty:
                df.columns = [c.strip() for c in df.columns]

        # Normaliser les ID (REF_PERSONNE, NUM_CONTRAT) en string pour comparaisons sûres
        self._normalize_ids()

        # Convertir les dates utiles en datetime64[ns]
        if 'DATE_NAISSANCE' in self.pp.columns:
            self.pp['DATE_NAISSANCE'] = pd.to_datetime(self.pp['DATE_NAISSANCE'], errors='coerce')

        if 'DATE_EXPIRATION' in self.contrats.columns:
            self.contrats['DATE_EXPIRATION'] = pd.to_datetime(self.contrats['DATE_EXPIRATION'], errors='coerce')

        if 'EFFET_CONTRAT' in self.contrats.columns:
            self.contrats['EFFET_CONTRAT'] = pd.to_datetime(self.contrats['EFFET_CONTRAT'], errors='coerce')

        for col in ['DATE_SURVENANCE', 'DATE_DECLARATION', 'DATE_OUVERTURE']:
            if col in self.sinistres.columns:
                self.sinistres[col] = pd.to_datetime(self.sinistres[col], errors='coerce')

        # Normaliser textes
        if 'LIB_PRODUIT' in self.contrats.columns:
            self.contrats['LIB_PRODUIT'] = self.contrats['LIB_PRODUIT'].fillna('').astype(str).str.strip()
        if 'LIB_BRANCHE' in self.contrats.columns:
            personnes_physiques=sheets.get('personne_physique', pd.DataFrame()),
            personnes_morales=sheets.get('personne_morale', pd.DataFrame()),
            contrats=sheets.get('Contrats', pd.DataFrame()),
            sinistres=sheets.get('sinistres', pd.DataFrame()),
            mapping_produits=sheets.get('Mapping_Produits', pd.DataFrame())
            self.contrats[col] = pd.to_numeric(self.contrats[col], errors='coerce').fillna(0.0)

        for col in ['MONTANT_ENCAISSE', 'MONTANT_A_ENCAISSER']:
            if col in self.sinistres.columns:
                self.sinistres[col] = pd.to_numeric(self.sinistres[col], errors='coerce').fillna(0.0)

    def _normalize_ids(self):
        """Force REF_PERSONNE and NUM_CONTRAT to str (trim)."""
        for df in [self.pp, self.pm]:
            if 'REF_PERSONNE' in df.columns:
                df['REF_PERSONNE'] = df['REF_PERSONNE'].astype(str).str.strip()

        if 'REF_PERSONNE' in self.contrats.columns:
            self.contrats['REF_PERSONNE'] = self.contrats['REF_PERSONNE'].astype(str).str.strip()
        if 'NUM_CONTRAT' in self.contrats.columns:
            self.contrats['NUM_CONTRAT'] = self.contrats['NUM_CONTRAT'].astype(str).str.strip()
        if 'NUM_CONTRAT' in self.sinistres.columns:
            self.sinistres['NUM_CONTRAT'] = self.sinistres['NUM_CONTRAT'].astype(str).str.strip()
        if 'LIB_PRODUIT' in self.mapping.columns:
            self.mapping['LIB_PRODUIT'] = self.mapping['LIB_PRODUIT'].astype(str).str.strip()

    # ------------------------- 
    # Fonctions d'extraction
    # -------------------------
    def _get_person_record(self, ref_personne: str) -> Dict[str, Any]:
        """Retourne dict d'info client (physique ou morale) ou {}."""
        ref_s = str(ref_personne).strip()
        rec = {}
        rpp = self.pp[self.pp['REF_PERSONNE'] == ref_s] if ('REF_PERSONNE' in self.pp.columns and not self.pp.empty) else pd.DataFrame()
        rpm = self.pm[self.pm['REF_PERSONNE'] == ref_s] if ('REF_PERSONNE' in self.pm.columns and not self.pm.empty) else pd.DataFrame()
        if not rpp.empty:
            row = rpp.iloc[0].to_dict()
            rec.update(row)
            rec['type_client'] = 'physique'
            if 'DATE_NAISSANCE' in rpp.columns and pd.notna(rpp.iloc[0].get('DATE_NAISSANCE')):
                try:
                    rec['AGE'] = int((pd.Timestamp.now() - rpp.iloc[0]['DATE_NAISSANCE']).days // 365)
                    if rec['AGE'] < 25:
                        rec['TRANCHE_AGE'] = 'Jeune'
                    elif 25 <= rec['AGE'] < 55:
                        rec['TRANCHE_AGE'] = 'Adulte'
                    else:
                        rec['TRANCHE_AGE'] = 'Senior'
                except Exception:
                    rec['AGE'] = None
                    rec['TRANCHE_AGE'] = None
        elif not rpm.empty:
            row = rpm.iloc[0].to_dict()
            rec.update(row)
            rec['type_client'] = 'morale'
            rec['AGE'] = None
            rec['TRANCHE_AGE'] = None
        else:
            return {}

        if 'CODE_SEXE' in rec:
            rec['SEXE'] = clean_nan_values(rec.get('CODE_SEXE'))
        if 'SITUATION_FAMILIALE' in rec:
            rec['SITUATION_FAMILIALE'] = clean_nan_values(rec.get('SITUATION_FAMILIALE'))
        if 'LIB_PROFESSION' in rec:
            rec['LIB_PROFESSION'] = clean_nan_values(rec.get('LIB_PROFESSION'))
        if 'VILLE' in rec:
            ville_value = clean_nan_values(rec.get('VILLE'))
            rec['VILLE'] = str(ville_value).strip() if ville_value is not None else ''
        if 'LIB_SECTEUR_ACTIVITE' in rec:
            rec['LIB_SECTEUR_ACTIVITE'] = clean_nan_values(rec.get('LIB_SECTEUR_ACTIVITE'))
        if 'LIEU_NAISSANCE' in rec:
            rec['LIEU_NAISSANCE'] = clean_nan_values(rec.get('LIEU_NAISSANCE'))
        if 'LIB_GOUVERNORAT' in rec:
            rec['LIB_GOUVERNORAT'] = clean_nan_values(rec.get('LIB_GOUVERNORAT'))
        if 'VILLE_GOUVERNORAT' in rec:
            rec['VILLE_GOUVERNORAT'] = clean_nan_values(rec.get('VILLE_GOUVERNORAT'))

        return rec

    def _contracts_for_person(self, ref_personne: str) -> pd.DataFrame:
        """Tous les contrats liés au REF_PERSONNE."""
        if self.contrats.empty or 'REF_PERSONNE' not in self.contrats.columns:
            return pd.DataFrame()
        ref_s = str(ref_personne).strip()
        return self.contrats[self.contrats['REF_PERSONNE'] == ref_s].copy()

    def _split_contracts(self, df_contracts: pd.DataFrame, reference_date: Optional[pd.Timestamp] = None) -> Dict[str, pd.DataFrame]:
        """Sépare en 'en_cours' et 'expires'."""
        if reference_date is None:
            reference_date = pd.Timestamp.now()
        if df_contracts.empty:
            return {'en_cours': pd.DataFrame(), 'expires': pd.DataFrame()}
        if 'DATE_EXPIRATION' not in df_contracts.columns:
            return {'en_cours': df_contracts.copy(), 'expires': pd.DataFrame()}
        df = df_contracts.copy()
        df['DATE_EXPIRATION'] = pd.to_datetime(df['DATE_EXPIRATION'], errors='coerce')
        en_cours = df[(df['DATE_EXPIRATION'].isna()) | (df['DATE_EXPIRATION'] >= reference_date)].copy()
        expires = df[(df['DATE_EXPIRATION'].notna()) & (df['DATE_EXPIRATION'] < reference_date)].copy()
        return {'en_cours': en_cours, 'expires': expires}

    def _sinistres_by_contract(self, num_contrat: str) -> List[Dict[str, Any]]:
        """Retourne la liste des sinistres liés à un contrat."""
        if self.sinistres.empty or 'NUM_CONTRAT' not in self.sinistres.columns:
            return []
        num_s = str(num_contrat).strip()
        s = self.sinistres[self.sinistres['NUM_CONTRAT'] == num_s].copy()
        if s.empty:
            return []
        cols_wanted = ['NUM_SINISTRE', 'NATURE_SINISTRE', 'LIB_TYPE_SINISTRE', 'TAUX_RESPONSABILITE',
                       'DATE_SURVENANCE', 'DATE_DECLARATION', 'DATE_OUVERTURE', 'LIB_ETAT_SINISTRE',
                       'MONTANT_ENCAISSE', 'MONTANT_A_ENCAISSER', 'OBSERVATION_SINISTRE', 'LIEU_ACCIDENT']
        recs = []
        for _, row in s.iterrows():
            rec = {}
            for c in cols_wanted:
                if c in s.columns:
                    v = row.get(c)
                    if c in ['DATE_SURVENANCE', 'DATE_DECLARATION', 'DATE_OUVERTURE'] and pd.notna(v):
                        rec[c] = v  # Keep as datetime for DataFrame operations
                    else:
                        rec[c] = clean_nan_values(v)
            recs.append(rec)
        return recs

    def _map_products(self, contracts_df: pd.DataFrame) -> pd.DataFrame:
        """Joins mapping_produits pour enrichir LIB_PRODUIT."""
        if contracts_df.empty:
            return pd.DataFrame()
        mp = self.mapping.copy()
        if mp.empty or 'LIB_PRODUIT' not in mp.columns:
            return contracts_df.copy()
        cpy = contracts_df.copy()
        cpy['LIB_PRODUIT_KEY'] = cpy.get('LIB_PRODUIT', '').astype(str).str.strip().str.upper()
        mp['LIB_PRODUIT_KEY'] = mp['LIB_PRODUIT'].astype(str).str.strip().str.upper()
        merged = cpy.merge(mp[['LIB_PRODUIT_KEY', 'LIB_BRANCHE', 'LIB_SOUS_BRANCHE', 'LIB_PRODUIT']],
                          on='LIB_PRODUIT_KEY', how='left', suffixes=('', '_mp'))
        if 'LIB_BRANCHE_mp' in merged.columns:
            merged['LIB_BRANCHE'] = merged['LIB_BRANCHE'].fillna(merged['LIB_BRANCHE_mp'])
        else:
            merged['LIB_BRANCHE'] = merged['LIB_BRANCHE'].fillna('Inconnu')
        if 'LIB_SOUS_BRANCHE_mp' in merged.columns:
            merged['LIB_SOUS_BRANCHE'] = merged['LIB_SOUS_BRANCHE'].fillna(merged['LIB_SOUS_BRANCHE_mp'])
        else:
            merged['LIB_SOUS_BRANCHE'] = merged['LIB_SOUS_BRANCHE'].fillna('Inconnu')
        for c in ['LIB_PRODUIT_KEY', 'LIB_PRODUIT_mp', 'LIB_BRANCHE_mp', 'LIB_SOUS_BRANCHE_mp']:
            if c in merged.columns:
                merged.drop(columns=[c], inplace=True)
        return merged

    # ------------------------- 
    # Analyse des données
    # -------------------------
    def _analyze_client_risk(self, all_contracts: pd.DataFrame, all_sinistres: pd.DataFrame) -> Dict[str, Any]:
        """Analyse les risques du client (ex: capital élevé, sinistres fréquents)."""
        risk_profile = {'high_capital': False, 'frequent_sinistres': False, 'unpaid_premiums': 0.0}
        if not all_contracts.empty and 'Capital_assure' in all_contracts.columns:
            capital_moyen = all_contracts['Capital_assure'].mean()
            if capital_moyen > 50000:
                risk_profile['high_capital'] = True
        if not all_sinistres.empty and 'DATE_SURVENANCE' in all_sinistres.columns:
            now = pd.Timestamp.now()
            all_sinistres['DATE_SURVENANCE'] = pd.to_datetime(all_sinistres['DATE_SURVENANCE'], errors='coerce')
            sinistres_recents = all_sinistres[all_sinistres['DATE_SURVENANCE'] >= (now - pd.DateOffset(years=2))]
            if len(sinistres_recents) > 2:
                risk_profile['frequent_sinistres'] = True
        if not all_contracts.empty and 'statut_paiement' in all_contracts.columns:
            unpaid = all_contracts[all_contracts['statut_paiement'] == 'Non payé']['somme_quittances'].sum()
            risk_profile['unpaid_premiums'] = float(unpaid)
        return risk_profile

    def _generate_payment_chart(self, contracts_df: pd.DataFrame, ref_personne: str, output_dir: str = 'charts') -> str:
        """Génère un pie chart pour les statuts de paiement et retourne le chemin du fichier."""
        if contracts_df.empty or 'statut_paiement' not in contracts_df.columns:
            return ''
        payment_counts = contracts_df['statut_paiement'].value_counts()
        labels = payment_counts.index
        sizes = payment_counts.values
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(f"Répartition des paiements pour REF_PERSONNE {ref_personne}")
        Path(output_dir).mkdir(exist_ok=True)
        chart_path = f"{output_dir}/payment_status_{ref_personne}.png"
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    def _generate_capital_chart(self, contracts_df: pd.DataFrame, ref_personne: str, output_dir: str = 'charts') -> str:
        """Génère un bar chart pour le capital assuré par contrat."""
        if contracts_df.empty or 'Capital_assure' not in contracts_df.columns or 'NUM_CONTRAT' not in contracts_df.columns:
            return ''
        capitals = contracts_df['Capital_assure']
        contracts = contracts_df['NUM_CONTRAT'].astype(str)
        plt.figure(figsize=(8, 6))
        plt.bar(contracts, capitals, color='skyblue')
        plt.xlabel('Numéro de contrat')
        plt.ylabel('Capital assuré')
        plt.title(f"Capital assuré par contrat pour REF_PERSONNE {ref_personne}")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        Path(output_dir).mkdir(exist_ok=True)
        chart_path = f"{output_dir}/capital_{ref_personne}.png"
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    def _generate_sinistres_trend_chart(self, sinistres_df: pd.DataFrame, ref_personne: str, output_dir: str = 'charts') -> str:
        """Génère un line chart pour le nombre de sinistres par année."""
        if sinistres_df.empty or 'DATE_SURVENANCE' not in sinistres_df.columns:
            return ''
        sinistres_df = sinistres_df.copy()
        sinistres_df['DATE_SURVENANCE'] = pd.to_datetime(sinistres_df['DATE_SURVENANCE'], errors='coerce')
        sinistres_df = sinistres_df[sinistres_df['DATE_SURVENANCE'].notna()]
        if sinistres_df.empty:
            return ''
        sinistres_df['YEAR'] = sinistres_df['DATE_SURVENANCE'].dt.year
        yearly_counts = sinistres_df['YEAR'].value_counts().sort_index()
        plt.figure(figsize=(8, 6))
        plt.plot(yearly_counts.index, yearly_counts.values, marker='o', linestyle='-')
        plt.xlabel('Année')
        plt.ylabel('Nombre de sinistres')
        plt.title(f"Tendance des sinistres pour REF_PERSONNE {ref_personne}")
        plt.grid(True)
        Path(output_dir).mkdir(exist_ok=True)
        chart_path = f"{output_dir}/sinistres_trend_{ref_personne}.png"
        plt.savefig(chart_path)
        plt.close()
        return chart_path

    # ------------------------- 
    # Scoring et segmentation
    # -------------------------
    def _calculate_client_score(self, client_info: Dict[str, Any], contracts_en_cours: pd.DataFrame, all_sinistres: pd.DataFrame, branches_possedes: set) -> Dict[str, Any]:
        """Calcule le score client basé sur différents critères."""
        client_score = 0
        score_reasons = []

        if client_info.get('TRANCHE_AGE') == 'Adulte':
            client_score += 2
            score_reasons.append('Age (Adulte): +2')
        elif client_info.get('TRANCHE_AGE') == 'Jeune':
            client_score += 1
            score_reasons.append('Age (Jeune): +1')

        nb_sinistres_total = len(all_sinistres)
        if nb_sinistres_total == 0:
            client_score += 3
            score_reasons.append('Aucun sinistre: +3')
        elif nb_sinistres_total <= 2:
            client_score += 1
            score_reasons.append('Peu de sinistres: +1')
        else:
            client_score -= 2
            score_reasons.append('Nombreux sinistres: -2')

        if not contracts_en_cours.empty and 'statut_paiement' in contracts_en_cours.columns:
            paid_contracts = contracts_en_cours[contracts_en_cours['statut_paiement'] == 'Payé']
            if len(paid_contracts) == len(contracts_en_cours):
                client_score += 2
                score_reasons.append('Paiements réguliers: +2')
            elif len(paid_contracts) > 0:
                client_score += 1
                score_reasons.append('Paiements partiels: +1')
            else:
                client_score -= 1
                score_reasons.append('Paiements irréguliers: -1')

        if len(branches_possedes) >= 3:
            client_score += 2
            score_reasons.append('Diversification produits: +2')
        elif len(branches_possedes) == 1:
            client_score -= 1
            score_reasons.append('Manque de diversification: -1')

        return {'CLIENT_SCORE': client_score, 'SCORE_REASONS': score_reasons}

    def _segment_client(self, client_score: int, nb_sinistres: int, payment_status: str) -> str:
        """Segmente le client en groupes."""
        if client_score >= 6 and nb_sinistres <= 1:
            return 'Premium'
        elif nb_sinistres > 3 or payment_status == 'Irrégulier':
            return 'Risque élevé'
        elif client_score >= 3:
            return 'À fidéliser'
        else:
            return 'Standard'

    def _detect_behaviors(self, all_contracts: pd.DataFrame, all_sinistres: pd.DataFrame, contracts_expired: pd.DataFrame) -> List[Dict[str, Any]]:
        """Détecte des comportements spécifiques."""
        behaviors = []
        if all_contracts.empty or (not contracts_expired.empty and all_contracts.empty):
            behaviors.append({
                'behavior': 'client_inactif',
                'description': 'Client sans contrats actifs',
                'recommendation': 'ACTION MARKETING REENGAGEMENT'
            })
        if not all_sinistres.empty and 'DATE_SURVENANCE' in all_sinistres.columns:
            now = pd.Timestamp.now()
            all_sinistres['DATE_SURVENANCE'] = pd.to_datetime(all_sinistres['DATE_SURVENANCE'], errors='coerce')
            sinistres_recents = all_sinistres[all_sinistres['DATE_SURVENANCE'] >= (now - pd.DateOffset(years=2))]
            if len(sinistres_recents) > 2:
                behaviors.append({
                    'behavior': 'sinistres_frequents',
                    'description': f'Fréquence de sinistres élevée: {len(sinistres_recents)} sinistres en 2 ans',
                    'recommendation': 'REVISION PRIME / SUIVI RISQUE'
                })
        if not all_contracts.empty and 'Capital_assure' in all_contracts.columns:
            capital_moyen = all_contracts['Capital_assure'].mean()
            if capital_moyen > 50000:
                behaviors.append({
                    'behavior': 'capital_eleve',
                    'description': f'Capital assuré moyen élevé: {capital_moyen:.2f}',
                    'recommendation': 'PROPOSITION MONTEE EN GAMME'
                })
        return behaviors

    # ------------------------- 
    # Moteur de règles amélioré
    # -------------------------
    def rule_opportunities(self, client_info: Dict[str, Any], contracts_en_cours: pd.DataFrame, contracts_expired: pd.DataFrame, all_contracts: pd.DataFrame, all_sinistres: pd.DataFrame) -> List[Dict[str, Any]]:
        """Moteur de règles pour détecter les opportunités."""
        ops = []
        if contracts_en_cours is None:
            contracts_en_cours = pd.DataFrame()
        possedes = set((contracts_en_cours.get('LIB_PRODUIT', pd.Series([], dtype=object)).fillna('')).astype(str).str.strip().str.upper().unique())
        branches_possedes = set((contracts_en_cours.get('LIB_BRANCHE', pd.Series([], dtype=object)).fillna('')).astype(str).str.strip().str.upper().unique())

        age = client_info.get('AGE')
        situation = str(client_info.get('SITUATION_FAMILIALE', '')).lower() if client_info.get('SITUATION_FAMILIALE') else ''
        profession = str(client_info.get('LIB_PROFESSION', '')).lower() if client_info.get('LIB_PROFESSION') else ''
        type_client = client_info.get('type_client')
        client_score = client_info.get('CLIENT_SCORE', 0)

        # Scoring
        scoring_result = self._calculate_client_score(client_info, contracts_en_cours, all_sinistres, branches_possedes)
        client_info.update(scoring_result)

        # Segmentation
        payment_status = 'Régulier'
        if not contracts_en_cours.empty and 'statut_paiement' in contracts_en_cours.columns:
            paid_contracts = contracts_en_cours[contracts_en_cours['statut_paiement'] == 'Payé']
            if len(paid_contracts) == 0:
                payment_status = 'Irrégulier'
            elif len(paid_contracts) < len(contracts_en_cours):
                payment_status = 'Partiel'
        client_segment = self._segment_client(scoring_result['CLIENT_SCORE'], len(all_sinistres), payment_status)
        client_info['CLIENT_SEGMENT'] = client_segment

        # Behaviors
        behaviors = self._detect_behaviors(all_contracts, all_sinistres, contracts_expired)
        client_info['BEHAVIORS'] = behaviors

        # Risk Analysis
        risk_profile = self._analyze_client_risk(all_contracts, all_sinistres)
        client_info['RISK_PROFILE'] = risk_profile

        # Ethical Safeguard: Cap recommendations for low-score clients
        max_recommendations = 3 if client_score >= 3 else 2

        # Existing Rules
        only_habitation = False
        if len(possedes) == 1:
            prod = list(possedes)[0] if possedes else ''
            if any(k in prod for k in ['HABITATION', 'MULTIRISQUE', 'MRH']):
                only_habitation = True
        if age is not None and age < 35 and only_habitation and ('couple' in situation or 'mari' in situation or 'marie' in situation):
            ops.append({
                'rule': 'jeune_couple_habitation',
                'recommendation': ['ASSURANCE VIE', 'ASSURANCE SANTE'],
                'reason': 'Jeune couple avec seulement une habitation'
            })

        if 'medecin' in profession and not any('RESPONSABILITE' in b for b in branches_possedes):
            ops.append({
                'rule': 'medecin_seulement_auto',
                'recommendation': ['RESPONSABILITE PROFESSIONNELLE', 'SANTE PRO'],
                'reason': 'Profession médicale détectée, vérifier couverture pro'
            })

        if not any('SANTE' in p for p in possedes):
            ops.append({
                'rule': 'manque_sante',
                'recommendation': ['ASSURANCE SANTE'],
                'reason': 'Pas de produit SANTE détecté'
            })

        if age is not None and age > 25 and not any('VIE' in p for p in possedes):
            ops.append({
                'rule': 'manque_vie',
                'recommendation': ['ASSURANCE VIE'],
                'reason': 'Pas de produit VIE détecté pour profil adulte'
            })

        if type_client == 'morale':
            if not any('COLLECTIF' in p or 'GROUP' in p for p in possedes):
                ops.append({
                    'rule': 'morale_offre_entreprise',
                    'recommendation': ['ASSURANCE COLLECTIVE', 'SANTE COLLECTIVE'],
                    'reason': 'Client entreprise sans offres collectives'
                })

        if not contracts_expired.empty:
            now = pd.Timestamp.now()
            recent = contracts_expired.copy()
            if 'DATE_EXPIRATION' in recent.columns:
                recent['DATE_EXPIRATION'] = pd.to_datetime(recent['DATE_EXPIRATION'], errors='coerce')
                recent_recent = recent[(now - recent['DATE_EXPIRATION']).dt.days <= 365]
                if not recent_recent.empty:
                    ops.append({
                        'rule': 'recent_expire',
                        'recommendation': ['RENOUVELLEMENT / PROPOSITION OFFRE AMELIOREE'],
                        'reason': 'Contrats expirés récemment'
                    })

        # New Rules: Life Events
        if ('mari' in situation or 'marie' in situation) and not any('VIE' in p for p in possedes):
            ops.append({
                'rule': 'married_no_life',
                'recommendation': ['ASSURANCE VIE', 'FAMILY BUNDLE'],
                'reason': 'Client marié sans assurance vie, proposer bundle familial'
            })

        if age is not None and age >= 55 and not any('CAPITALISATION' in p for p in possedes):
            ops.append({
                'rule': 'senior_retirement',
                'recommendation': ['ASSURANCE VIE COMPLEMENT RETRAITE - HORIZON'],
                'reason': 'Client senior sans produit de capitalisation pour la retraite'
            })

        # New Rule: Bundling
        if len(branches_possedes) == 1 and 'AUTOMOBILE' in branches_possedes:
            ops.append({
                'rule': 'auto_only_bundle',
                'recommendation': ['BUNDLE AUTO + SANTE', 'BUNDLE AUTO + VIE'],
                'reason': 'Client avec seulement automobile, proposer bundle pour réduction'
            })

        # Segment-Based Rules
        if client_segment == 'Premium':
            ops.append({
                'rule': 'client_premium',
                'recommendation': ['OFFRES EXCLUSIVES', 'SERVICES VIP'],
                'reason': 'Client premium avec excellent profil'
            })
        elif client_segment == 'Risque élevé':
            ops.append({
                'rule': 'client_risque',
                'recommendation': ['REVISION CONDITIONS', 'SUIVI RENFORCE'],
                'reason': 'Client à risque élevé nécessitant un suivi'
            })

        # Ethical Safeguard: Limit recommendations
        seen = set()
        final_ops = []
        for o in ops[:max_recommendations]:
            key = tuple(sorted(o['recommendation']))
            if key not in seen:
                final_ops.append(o)
                seen.add(key)
        return final_ops

    # ------------------------- 
    # Sortie principale
    # -------------------------
    def get_client_profile(self, ref_personne: str, reference_date: Optional[pd.Timestamp] = None) -> Dict[str, Any]:
        """Génère le profil client complet."""
        if reference_date is None:
            reference_date = pd.Timestamp.now()

        client = self._get_person_record(ref_personne)
        if not client:
            return {'error': f'REF_PERSONNE {ref_personne} non trouvé'}

        all_contracts = self._contracts_for_person(ref_personne)
        split = self._split_contracts(all_contracts, reference_date=reference_date)
        en_cours = split['en_cours']
        expires = split['expires']

        en_cours_m = self._map_products(en_cours) if not en_cours.empty else en_cours
        expires_m = self._map_products(expires) if not expires.empty else expires

        all_sinistres_for_person = []
        if not all_contracts.empty and 'NUM_CONTRAT' in all_contracts.columns:
            for num_contrat in all_contracts['NUM_CONTRAT'].unique():
                if pd.notna(num_contrat):
                    contract_sinistres = self.sinistres[self.sinistres['NUM_CONTRAT'] == str(num_contrat).strip()].copy()
                    if not contract_sinistres.empty:
                        all_sinistres_for_person.append(contract_sinistres)
        all_sinistres_for_person = pd.concat(all_sinistres_for_person, ignore_index=True) if all_sinistres_for_person else pd.DataFrame()

        def contract_row_to_dict(r):
            cols = ['NUM_CONTRAT', 'LIB_PRODUIT', 'LIB_BRANCHE', 'LIB_SOUS_BRANCHE',
                    'EFFET_CONTRAT', 'DATE_EXPIRATION', 'PROCHAIN_TERME', 'LIB_ETAT_CONTRAT',
                    'somme_quittances', 'statut_paiement', 'Capital_assure']
            rec = {}
            for c in cols:
                if c in r.index:
                    v = r[c]
                    if c in ['EFFET_CONTRAT', 'DATE_EXPIRATION', 'PROCHAIN_TERME'] and pd.notna(v):
                        rec[c] = v.isoformat() if isinstance(v, (pd.Timestamp, np.datetime64)) else clean_nan_values(v)
                    else:
                        rec[c] = clean_nan_values(v)
            return rec

        contrats_en_cours_list = [contract_row_to_dict(row) for _, row in en_cours_m.iterrows()] if not en_cours_m.empty else []
        contrats_expired_list = [contract_row_to_dict(row) for _, row in expires_m.iterrows()] if not expires_m.empty else []

        sinistres_info = []
        for _, row in all_contracts.iterrows():
            num = row.get('NUM_CONTRAT')
            if pd.notna(num):
                sins = self._sinistres_by_contract(num)
                if sins:
                    # Convert dates to ISO format for JSON serialization
                    for sin in sins:
                        for date_col in ['DATE_SURVENANCE', 'DATE_DECLARATION', 'DATE_OUVERTURE']:
                            if date_col in sin and isinstance(sin[date_col], (pd.Timestamp, np.datetime64)):
                                sin[date_col] = sin[date_col].isoformat()
                    sinistres_info.append({'NUM_CONTRAT': str(num), 'sinistres': sins})

        total_capital_assure = float(all_contracts['Capital_assure'].sum()) if 'Capital_assure' in all_contracts.columns else 0.0
        nb_contrats_actifs = int(len(en_cours)) if en_cours is not None else 0
        nb_contrats_total = int(len(all_contracts)) if all_contracts is not None else 0

        opportunities = self.rule_opportunities(client, en_cours_m, expires_m, all_contracts, all_sinistres_for_person)


        # --- Génération de graphiques utiles et modernes ---
        
        charts_dir = os.path.join(os.path.dirname(__file__), '../../charts')
        os.makedirs(charts_dir, exist_ok=True)
        chart_paths = {}

        # 1. Bar chart: Répartition des contrats par type
        contract_types = Counter([c.get('LIB_PRODUIT') for c in contrats_en_cours_list + contrats_expired_list if c.get('LIB_PRODUIT')])
        if contract_types:
            plt.figure(figsize=(6,4))
            plt.bar(contract_types.keys(), contract_types.values(), color='#4f98ca')
            plt.title('Répartition des contrats par type')
            plt.xlabel('Type de contrat')
            plt.ylabel('Nombre')
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()
            chart1_path = os.path.join(charts_dir, f"contracts_by_type_{ref_personne}.png")
            plt.savefig(chart1_path)
            plt.close()
            chart_paths['contracts_by_type'] = chart1_path

        # 2. Pie chart: Statut des paiements
        pay_status = Counter(c.get('statut_paiement', 'Inconnu') for c in contrats_en_cours_list)
        if pay_status:
            plt.figure(figsize=(5,5))
            plt.pie(pay_status.values(), labels=pay_status.keys(), autopct='%1.1f%%', startangle=90, colors=['#8fd9b6','#f7b267','#f4845f','#4f98ca'])
            plt.title('Statut des paiements (contrats en cours)')
            plt.tight_layout()
            chart2_path = os.path.join(charts_dir, f"payment_status_{ref_personne}.png")
            plt.savefig(chart2_path)
            plt.close()
            chart_paths['payment_status'] = chart2_path

        # 3. Line chart: Capital assuré au fil du temps
        cap_dates = [(c.get('EFFET_CONTRAT'), c.get('Capital_assure', 0)) for c in contrats_en_cours_list if c.get('EFFET_CONTRAT')]
       
        if cap_dates:
            df_cap = pd.DataFrame(cap_dates, columns=['date','capital'])
            df_cap['date'] = pd.to_datetime(df_cap['date'], errors='coerce')
            df_cap = df_cap.sort_values('date')
            plt.figure(figsize=(7,4))
            plt.plot(df_cap['date'], df_cap['capital'], marker='o', color='#f4845f')
            plt.title('Capital assuré au fil du temps')
            plt.xlabel('Date effet contrat')
            plt.ylabel('Capital assuré')
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.tight_layout()
            chart3_path = os.path.join(charts_dir, f"capital_trend_{ref_personne}.png")
            plt.savefig(chart3_path)
            plt.close()
            chart_paths['capital_trend'] = chart3_path

        # 4. Bar chart: Nombre de sinistres par année
        sinistres_years = []
        for s in sinistres_info:
            for sin in s.get('sinistres', []):
                date = sin.get('DATE_SURVENANCE')
                if date:
                    try:
                        year = pd.to_datetime(date).year
                        sinistres_years.append(year)
                    except Exception:
                        pass
        if sinistres_years:
            year_counts = Counter(sinistres_years)
            plt.figure(figsize=(6,4))
            plt.bar(year_counts.keys(), year_counts.values(), color='#8fd9b6')
            plt.title('Nombre de sinistres par année')
            plt.xlabel('Année')
            plt.ylabel('Nombre de sinistres')
            plt.tight_layout()
            chart4_path = os.path.join(charts_dir, f"sinistres_per_year_{ref_personne}.png")
            plt.savefig(chart4_path)
            plt.close()
            chart_paths['sinistres_per_year'] = chart4_path

        charts = chart_paths

        summary_lines = []
        summary_lines.append(f"Client REF_PERSONNE={ref_personne}, type={client.get('type_client')}, nom={client.get('NOM') or client.get('NOM_PRENOM')}")
        if client.get('AGE') is not None:
            summary_lines.append(f"Age: {client.get('AGE')} ({client.get('TRANCHE_AGE')})")
        if client.get('LIB_PROFESSION'):
            summary_lines.append(f"Profession: {client.get('LIB_PROFESSION')}")
        if client.get('LIB_SECTEUR_ACTIVITE'):
            summary_lines.append(f"Secteur: {client.get('LIB_SECTEUR_ACTIVITE')}")
        ville_display = client.get('VILLE') if client.get('VILLE') else 'Non renseigné'
        summary_lines.append(f"Ville: {ville_display}")
        summary_lines.append(f"Nb contrats actifs: {nb_contrats_actifs}, total contrats: {nb_contrats_total}, capital_total: {total_capital_assure:.2f}")
        summary_lines.append(f"Score Client: {client.get('CLIENT_SCORE')} (Raisons: {', '.join(client.get('SCORE_REASONS', []))})")
        summary_lines.append(f"Segment Client: {client.get('CLIENT_SEGMENT')}")
        if client.get('RISK_PROFILE'):
            summary_lines.append(f"Profil de risque: Capital élevé={client['RISK_PROFILE']['high_capital']}, Sinistres fréquents={client['RISK_PROFILE']['frequent_sinistres']}, Impayés={client['RISK_PROFILE']['unpaid_premiums']:.2f}")
        if client.get('BEHAVIORS'):
            summary_lines.append("Comportements détectés:")
            for behavior in client.get('BEHAVIORS', []):
                summary_lines.append(f"- {behavior['description']} -> {behavior['recommendation']}")
        if contrats_en_cours_list:
            summary_lines.append("Contrats en cours:")
            for c in contrats_en_cours_list:
                summary_lines.append(f"- {c.get('NUM_CONTRAT')} | {c.get('LIB_PRODUIT')} | branche={c.get('LIB_BRANCHE')} | capital={c.get('Capital_assure')} | paiement={c.get('statut_paiement')}")
        if contrats_expired_list:
            summary_lines.append("Contrats expirés:")
            for c in contrats_expired_list:
                summary_lines.append(f"- {c.get('NUM_CONTRAT')} | {c.get('LIB_PRODUIT')} | branche={c.get('LIB_BRANCHE')} | expiration={c.get('DATE_EXPIRATION')} | paiement={c.get('statut_paiement')}")
        if sinistres_info:
            summary_lines.append("Sinistres:")
            for s in sinistres_info:
                summary_lines.append(f"- Contrat {s['NUM_CONTRAT']}: {len(s['sinistres'])} sinistres (ex: montants: {[x.get('MONTANT_A_ENCAISSER') for x in s['sinistres']][:3]})")
        if opportunities:
            summary_lines.append("Opportunités détectées:")
            for op in opportunities:
                summary_lines.append(f"- {op['reason']} -> {', '.join(op['recommendation'])}")
        if any(charts.values()):
            summary_lines.append("Graphiques générés:")
            for chart_name, chart_path in charts.items():
                if chart_path:
                    summary_lines.append(f"- {chart_name}: {chart_path}")

        summary_text = "\n".join(summary_lines)

        result = {
            'REF_PERSONNE': str(ref_personne),
            'client_info': client,
            'contrats_en_cours': contrats_en_cours_list,
            'contrats_expired': contrats_expired_list,
            'sinistres': sinistres_info,
            'total_capital_assure': total_capital_assure,
            'nb_contrats_actifs': nb_contrats_actifs,
            'nb_contrats_total': nb_contrats_total,
            'opportunities': opportunities,
            'summary_text': summary_text,
            'charts': charts
        }
        return result

    # Placeholder for ML Integration
    def prepare_ml_data(self, ref_personne: str) -> Dict[str, Any]:
        """Prépare les données pour un futur modèle ML (ex: clustering)."""
        profile = self.get_client_profile(ref_personne)
        ml_features = {
            'AGE': profile['client_info'].get('AGE', None),
            'CLIENT_SCORE': profile['client_info'].get('CLIENT_SCORE', 0),
            'NB_SINISTRES': len(profile.get('sinistres', [])),
            'TOTAL_CAPITAL': profile.get('total_capital_assure', 0.0),
            'NB_CONTRATS': profile.get('nb_contrats_total', 0),
            'UNPAID_PREMIUMS': profile['client_info'].get('RISK_PROFILE', {}).get('unpaid_premiums', 0.0)
        }
        return ml_features

# ------------------------- 
# CLI / main
# -------------------------
def analyseDB(ref: str, xlsx_path: str = None):
    """Fonction principale pour exécuter l'analyse."""
    if xlsx_path is None:
        # Use a path relative to this script for portability
        xlsx_path = str(Path(__file__).parent.parent / "BD" / "new_data.xlsx")
    out_path = f"out_{ref}_final.json"
    sheets = load_excel_sheets(xlsx_path)
    extractor = ClientDataExtractor(
        personnes_physiques=sheets.get('personne_physique', pd.DataFrame()),
        personnes_morales=sheets.get('personne_morale', pd.DataFrame()),
        contrats=sheets.get('Contrats', pd.DataFrame()),
        sinistres=sheets.get('sinistres', pd.DataFrame()),
        mapping_produits=sheets.get('Mapping_Produits', pd.DataFrame())
    )

    profile = extractor.get_client_profile(ref_personne=ref)
    print("=== Résumé (pour LLM) ===")
    print(profile.get('summary_text', ''))

    json_text = json.dumps(profile, indent=2, ensure_ascii=False, default=str)
    if out_path:
        if not out_path.lower().endswith('.json'):
            out_path = out_path + '.json'
        Path(out_path).write_text(json_text, encoding='utf-8')
        print(f"JSON de sortie sauvegardé dans {out_path}")
    else:
        print("\n=== JSON complet ===")
        print(json_text)

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        ref = sys.argv[1]
        analyseDB(ref)
    else:
        print("Usage: python analyseDB_tool_updated.py <REF_PERSONNE>")
