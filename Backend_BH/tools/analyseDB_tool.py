#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client_data_tool_fixed.py
Version corrigée et plus robuste du tool d'extraction client.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

import pandas as pd
import numpy as np


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
        self.pp = personnes_physiques.copy() if personnes_physiques is not None else pd.DataFrame()
        self.pm = personnes_morales.copy() if personnes_morales is not None else pd.DataFrame()
        self.contrats = contrats.copy() if contrats is not None else pd.DataFrame()
        self.sinistres = sinistres.copy() if sinistres is not None else pd.DataFrame()
        self.mapping = mapping_produits.copy() if mapping_produits is not None else pd.DataFrame()

        # Normalisations de base : enlever espaces dans les noms de colonnes
        for df in [self.pp, self.pm, self.contrats, self.sinistres, self.mapping]:
            if not df.empty:
                df.columns = [c.strip() for c in df.columns]

        # Normaliser les ID (REF_PERSONNE, NUM_CONTRAT) en string pour comparaisons sûres
        self._normalize_ids()

        # Convertir les dates utiles
        if 'DATE_NAISSANCE' in self.pp.columns:
            self.pp['DATE_NAISSANCE'] = safe_to_datetime(self.pp['DATE_NAISSANCE'])

        if 'DATE_EXPIRATION' in self.contrats.columns:
            self.contrats['DATE_EXPIRATION'] = safe_to_datetime(self.contrats['DATE_EXPIRATION'])

        if 'EFFET_CONTRAT' in self.contrats.columns:
            self.contrats['EFFET_CONTRAT'] = safe_to_datetime(self.contrats['EFFET_CONTRAT'])

        for col in ['DATE_SURVENANCE', 'DATE_DECLARATION', 'DATE_OUVERTURE']:
            if col in self.sinistres.columns:
                self.sinistres[col] = safe_to_datetime(self.sinistres[col])

        # Normaliser textes
        if 'LIB_PRODUIT' in self.contrats.columns:
            self.contrats['LIB_PRODUIT'] = self.contrats['LIB_PRODUIT'].fillna('').astype(str).str.strip()
        if 'LIB_BRANCHE' in self.contrats.columns:
            self.contrats['LIB_BRANCHE'] = self.contrats['LIB_BRANCHE'].fillna('').astype(str).str.strip()

        # Ensure numeric columns
        for col in ['somme_quittances', 'Capital_assure']:
            if col in self.contrats.columns:
                self.contrats[col] = pd.to_numeric(self.contrats[col], errors='coerce').fillna(0.0)

        for col in ['MONTANT_ENCAISSE', 'MONTANT_A_ENCAISSER']:
            if col in self.sinistres.columns:
                self.sinistres[col] = pd.to_numeric(self.sinistres[col], errors='coerce').fillna(0.0)

    def _normalize_ids(self):
        """Force REF_PERSONNE and NUM_CONTRAT to str (trim)."""
        # REF_PERSONNE in personnes
        for df in [self.pp, self.pm]:
            if not df.empty and 'REF_PERSONNE' in df.columns:
                df['REF_PERSONNE'] = df['REF_PERSONNE'].astype(str).str.strip()

        # REF_PERSONNE in contrats
        if not self.contrats.empty and 'REF_PERSONNE' in self.contrats.columns:
            self.contrats['REF_PERSONNE'] = self.contrats['REF_PERSONNE'].astype(str).str.strip()
        # NUM_CONTRAT in contrats
        if not self.contrats.empty and 'NUM_CONTRAT' in self.contrats.columns:
            self.contrats['NUM_CONTRAT'] = self.contrats['NUM_CONTRAT'].astype(str).str.strip()
        # NUM_CONTRAT in sinistres
        if not self.sinistres.empty and 'NUM_CONTRAT' in self.sinistres.columns:
            self.sinistres['NUM_CONTRAT'] = self.sinistres['NUM_CONTRAT'].astype(str).str.strip()
        # If mapping exists, normalize product key
        if not self.mapping.empty and 'LIB_PRODUIT' in self.mapping.columns:
            self.mapping['LIB_PRODUIT'] = self.mapping['LIB_PRODUIT'].astype(str).str.strip()

    # -------------------------
    # Fonctions d'extraction
    # -------------------------
    def _get_person_record(self, ref_personne: str) -> Dict[str, Any]:
        """Retourne dict d'info client (physique ou morale) ou {}."""
        # Normalize input id to str trimmed
        ref_s = str(ref_personne).strip()
        rec = {}
        rpp = self.pp[self.pp['REF_PERSONNE'] == ref_s] if ('REF_PERSONNE' in self.pp.columns and not self.pp.empty) else pd.DataFrame()
        rpm = self.pm[self.pm['REF_PERSONNE'] == ref_s] if ('REF_PERSONNE' in self.pm.columns and not self.pm.empty) else pd.DataFrame()
        if not rpp.empty:
            row = rpp.iloc[0].to_dict()
            rec.update(row)
            rec['type_client'] = 'physique'
            # âge si possible
            if 'DATE_NAISSANCE' in rpp.columns and pd.notna(rpp.iloc[0].get('DATE_NAISSANCE')):
                try:
                    rec['AGE'] = int((pd.Timestamp.now() - rpp.iloc[0]['DATE_NAISSANCE']).days // 365)
                except Exception:
                    rec['AGE'] = None
        elif not rpm.empty:
            row = rpm.iloc[0].to_dict()
            rec.update(row)
            rec['type_client'] = 'morale'
            rec['AGE'] = None
        else:
            return {}
        # Normaliser colonnes utiles (copier si exist)
        if 'CODE_SEXE' in rec:
            rec['SEXE'] = rec.get('CODE_SEXE', None)
        if 'SITUATION_FAMILIALE' in rec:
            rec['SITUATION_FAMILIALE'] = rec.get('SITUATION_FAMILIALE', None)
        if 'LIB_PROFESSION' in rec:
            rec['LIB_PROFESSION'] = rec.get('LIB_PROFESSION', None)
        if 'VILLE' in rec:
            rec['VILLE'] = str(rec.get('VILLE', '')).strip()
        if 'LIB_SECTEUR_ACTIVITE' in rec:
            rec['LIB_SECTEUR_ACTIVITE'] = rec.get('LIB_SECTEUR_ACTIVITE', None)
        return rec

    def _contracts_for_person(self, ref_personne: str) -> pd.DataFrame:
        """Tous les contrats liés au REF_PERSONNE (possibilité que REF absent)."""
        if self.contrats.empty or 'REF_PERSONNE' not in self.contrats.columns:
            return pd.DataFrame()
        ref_s = str(ref_personne).strip()
        return self.contrats[self.contrats['REF_PERSONNE'] == ref_s].copy()

    def _split_contracts(self, df_contracts: pd.DataFrame, reference_date: Optional[pd.Timestamp] = None) -> Dict[str, pd.DataFrame]:
        """Sépare en 'en_cours' (expiration >= reference_date or NaT) et 'expires' (<)."""
        if reference_date is None:
            reference_date = pd.Timestamp.now()
        if df_contracts is None or df_contracts.empty:
            return {'en_cours': pd.DataFrame(), 'expires': pd.DataFrame()}
        # If no DATE_EXPIRATION column, treat all as en_cours
        if 'DATE_EXPIRATION' not in df_contracts.columns:
            return {'en_cours': df_contracts.copy(), 'expires': df_contracts.iloc[0:0].copy()}
        # Consider NaT as active (no expiration known)
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
                    if isinstance(v, (pd.Timestamp, np.datetime64)):
                        v = pd.to_datetime(v).isoformat()
                    rec[c] = v
            recs.append(rec)
        return recs

    def _map_products(self, contracts_df: pd.DataFrame) -> pd.DataFrame:
        """Joins mapping_produits pour enrichir LIB_PRODUIT si possible."""
        if contracts_df is None or contracts_df.empty:
            return contracts_df.copy() if isinstance(contracts_df, pd.DataFrame) else pd.DataFrame()
        mp = self.mapping.copy()
        if mp.empty or 'LIB_PRODUIT' not in mp.columns:
            return contracts_df.copy()
        # Prepare keys
        cpy = contracts_df.copy()
        cpy['LIB_PRODUIT_KEY'] = cpy.get('LIB_PRODUIT', '').astype(str).str.strip().str.upper()
        mp['LIB_PRODUIT_KEY'] = mp['LIB_PRODUIT'].astype(str).str.strip().str.upper()
        merged = cpy.merge(mp[['LIB_PRODUIT_KEY', 'LIB_BRANCHE', 'LIB_SOUS_BRANCHE', 'LIB_PRODUIT']],
                        on='LIB_PRODUIT_KEY', how='left', suffixes=('', '_mp'))

        # Fill missing LIB_BRANCHE avec colonne mp si existe, sinon valeur par défaut
        if 'LIB_BRANCHE_mp' in merged.columns:
            merged['LIB_BRANCHE'] = merged['LIB_BRANCHE'].fillna(merged['LIB_BRANCHE_mp'])
        else:
            merged['LIB_BRANCHE'] = merged['LIB_BRANCHE'].fillna('Inconnu')

        # Même chose pour LIB_SOUS_BRANCHE, avec fallback plus sûr
        if 'LIB_SOUS_BRANCHE_mp' in merged.columns:
            merged['LIB_SOUS_BRANCHE'] = merged['LIB_SOUS_BRANCHE'].fillna(merged['LIB_SOUS_BRANCHE_mp'])
        else:
            merged['LIB_SOUS_BRANCHE'] = merged['LIB_SOUS_BRANCHE'].fillna('Inconnu')

        # Supprimer colonnes auxiliaires si présentes
        for c in ['LIB_PRODUIT_KEY', 'LIB_PRODUIT_mp', 'LIB_BRANCHE_mp', 'LIB_SOUS_BRANCHE_mp']:
            if c in merged.columns:
                merged.drop(columns=[c], inplace=True)
        return merged


    # -------------------------
    # Moteur de règles simple
    # -------------------------
    def rule_opportunities(self, client_info: Dict[str, Any], contracts_en_cours: pd.DataFrame, contracts_expired: pd.DataFrame) -> List[Dict[str, Any]]:
        ops = []
        # handle empty
        if contracts_en_cours is None:
            contracts_en_cours = pd.DataFrame()
        possedes = set((contracts_en_cours.get('LIB_PRODUIT', pd.Series([], dtype=object)).fillna('')).astype(str).str.strip().str.upper().unique())
        branches_possedes = set((contracts_en_cours.get('LIB_BRANCHE', pd.Series([], dtype=object)).fillna('')).astype(str).str.strip().str.upper().unique())

        age = client_info.get('AGE')
        situation = str(client_info.get('SITUATION_FAMILIALE', '')).lower() if client_info.get('SITUATION_FAMILIALE') is not None else ''
        profession = str(client_info.get('LIB_PROFESSION', '')).lower() if client_info.get('LIB_PROFESSION') is not None else ''
        type_client = client_info.get('type_client')

        # Rule: jeune couple with only habitation => proposer VIE/SANTE
        only_habitation = False
        if len(possedes) == 1:
            prod = list(possedes)[0] if possedes else ''
            if any(k in prod for k in ['HABIT', 'HABITATION', 'MULTIRISQUE', 'MRH']):
                only_habitation = True
        if age is not None and age < 35 and only_habitation and ('couple' in situation or 'mari' in situation or 'marie' in situation):
            ops.append({'rule': 'jeune_couple_habitation', 'recommendation': ['ASSURANCE VIE', 'ASSURANCE SANTE'], 'reason': 'Jeune couple avec seulement une habitation'})

        # Rule: medecin
        if 'medecin' in profession and not any('RESPONSABILITE' in b for b in branches_possedes):
            ops.append({'rule': 'medecin_seulement_auto', 'recommendation': ['RESPONSABILITE PROFESSIONNELLE', 'SANTE PRO'], 'reason': 'Profession médicale détectée, vérifier couverture pro'})

        # Rule: manque SANTE
        if not any('SANTE' in p for p in possedes):
            ops.append({'rule': 'manque_sante', 'recommendation': ['ASSURANCE SANTE'], 'reason': 'Pas de produit SANTE détecté'})

        # Rule: manque VIE pour certain age
        if age is not None and age > 25 and not any('VIE' in p for p in possedes):
            ops.append({'rule': 'manque_vie', 'recommendation': ['ASSURANCE VIE'], 'reason': 'Pas de produit VIE détecté pour profil adulte'})

        # Rule: clients morales -> proposer produits entreprises si pas présents
        if type_client == 'morale':
            if not any('COLLECTIF' in p or 'GROUP' in p for p in possedes):
                ops.append({'rule': 'morale_offre_entreprise', 'recommendation': ['ASSURANCE COLLECTIVE', 'SANTE COLLECTIVE'], 'reason': 'Client entreprise sans offres collectives'})

        # Rule: contrats expirés récents -> proposer renouvellement
        if contracts_expired is not None and not contracts_expired.empty:
            now = pd.Timestamp.now()
            recent = contracts_expired.copy()
            if 'DATE_EXPIRATION' in recent.columns:
                recent['DATE_EXPIRATION'] = pd.to_datetime(recent['DATE_EXPIRATION'], errors='coerce')
                recent_recent = recent[(now - recent['DATE_EXPIRATION']).dt.days <= 365]
                if not recent_recent.empty:
                    ops.append({'rule': 'recent_expire', 'recommendation': ['RENOUVELLEMENT / PROPOSITION OFFRE AMELIOREE'], 'reason': 'Contrats expirés récemment'})

        # Dé-dup recommandations similaires
        seen = set()
        final_ops = []
        for o in ops:
            key = tuple(sorted(o['recommendation']))
            if key not in seen:
                final_ops.append(o)
                seen.add(key)
        return final_ops

    # -------------------------
    # Sortie principale
    # -------------------------
    def get_client_profile(self, ref_personne: str, reference_date: Optional[pd.Timestamp] = None) -> Dict[str, Any]:
        if reference_date is None:
            reference_date = pd.Timestamp.now()

        client = self._get_person_record(ref_personne)
        if not client:
            return {'error': f'REF_PERSONNE {ref_personne} non trouvé'}

        all_contracts = self._contracts_for_person(ref_personne)
        split = self._split_contracts(all_contracts, reference_date=reference_date)
        en_cours = split['en_cours']
        expires = split['expires']

        # Enrichir par mapping produits
        en_cours_m = self._map_products(en_cours) if not en_cours.empty else en_cours
        expires_m = self._map_products(expires) if not expires.empty else expires

        # Build contract dict lists
        def contract_row_to_dict(r):
            cols = ['NUM_CONTRAT', 'LIB_PRODUIT', 'LIB_BRANCHE', 'LIB_SOUS_BRANCHE',
                    'EFFET_CONTRAT', 'DATE_EXPIRATION', 'PROCHAIN_TERME', 'LIB_ETAT_CONTRAT',
                    'somme_quittances', 'statut_paiement', 'Capital_assure']
            rec = {}
            for c in cols:
                if c in r.index:
                    v = r[c]
                    if isinstance(v, (pd.Timestamp, np.datetime64)):
                        rec[c] = pd.to_datetime(v).isoformat()
                    else:
                        rec[c] = v if pd.notna(v) else None
            return rec

        contrats_en_cours_list = [contract_row_to_dict(row) for _, row in en_cours_m.iterrows()] if not en_cours_m.empty else []
        contrats_expired_list = [contract_row_to_dict(row) for _, row in expires_m.iterrows()] if not expires_m.empty else []

        # Sinistres per contract
        sinistres_info = []
        for _, row in all_contracts.iterrows():
            num = row.get('NUM_CONTRAT')
            if pd.notna(num):
                sins = self._sinistres_by_contract(num)
                if sins:
                    sinistres_info.append({'NUM_CONTRAT': str(num), 'sinistres': sins})

        # Calculs agrégés
        total_capital_assure = float(all_contracts['Capital_assure'].sum()) if 'Capital_assure' in all_contracts.columns else 0.0
        nb_contrats_actifs = int(len(en_cours)) if en_cours is not None else 0
        nb_contrats_total = int(len(all_contracts)) if all_contracts is not None else 0

        # Règles / opportunités
        opportunities = self.rule_opportunities(client, en_cours_m if not en_cours_m.empty else pd.DataFrame(), expires_m if not expires_m.empty else pd.DataFrame())

        # Synthèse texte pour LLM
        summary_lines = []
        summary_lines.append(f"Client REF_PERSONNE={ref_personne}, type={client.get('type_client')}, nom={client.get('NOM') or client.get('NOM_PRENOM')}")
        if client.get('AGE') is not None:
            summary_lines.append(f"Age: {client.get('AGE')}")
        if client.get('LIB_PROFESSION'):
            summary_lines.append(f"Profession: {client.get('LIB_PROFESSION')}")
        if client.get('LIB_SECTEUR_ACTIVITE'):
            summary_lines.append(f"Secteur: {client.get('LIB_SECTEUR_ACTIVITE')}")
        summary_lines.append(f"Ville: {client.get('VILLE')}")
        summary_lines.append(f"Nb contrats actifs: {nb_contrats_actifs}, total contrats: {nb_contrats_total}, capital_total: {total_capital_assure:.2f}")

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
            'summary_text': summary_text
        }
        return result


# -------------------------
# CLI / main
# -------------------------
from langchain_core.tools import tool
@tool
def analyseDB(
        ref: str,
):
    """
    Fonction principale pour exécuter l'analyse de la base de données client.

    """
    XLSX_PATH = "D:/fezaimohamedelamine/ia_genrative/BHAssurance/BD/new_data.xlsx"
    out_path = "out"+ref + ".json"

    sheets = load_excel_sheets(XLSX_PATH)
    extractor = ClientDataExtractor(
        personnes_physiques=sheets.get('personne_physique', pd.DataFrame()),
        personnes_morales=sheets.get('personne_morale', pd.DataFrame()),
        contrats=sheets.get('Contrats', pd.DataFrame()),
        sinistres=sheets.get('sinistres', pd.DataFrame()),
        mapping_produits=sheets.get('Mapping_Produits', pd.DataFrame())
    )

    profile = extractor.get_client_profile(ref_personne=ref)
    # Print summary text
    #print("=== Résumé (pour LLM) ===")
    #print(profile.get('summary_text', ''))
    return profile

    # Dump JSON
""" json_text = json.dumps(profile, indent=2, ensure_ascii=False, default=str)
    if out_path:
        # ensure .json extension
        if not out_path.lower().endswith('.json'):
            out_path = out_path + '.json'
        Path(out_path).write_text(json_text, encoding='utf-8')
        print(f"JSON de sortie sauvegardé dans {out_path}")
    else:
        print("\n=== JSON complet ===")
        print(json_text)
"""
#analyseDB("1381")  # 
