document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('resultContainer');
    const errorContainer = document.getElementById('errorContainer');
    
    // Initialiser window.scoreChart comme null au début
    window.scoreChart = null;
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const refClient = document.getElementById('ref_client').value.trim();
        if (!refClient) {
            showError("Veuillez entrer une référence client");
            return;
        }
        
        // Afficher le loader
        loading.classList.remove('hidden');
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        
        // Envoyer la requête au serveur
        fetch('/get_recommendation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `ref_client=${encodeURIComponent(refClient)}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau');
            }
            return response.json();
        })
        .then(data => {
            loading.classList.add('hidden');
            
            if (data.status === "error") {
                showError(data.message);
                return;
            }
            
            // Afficher les résultats
            displayResults(data.data);
            resultContainer.classList.remove('hidden');
        })
        .catch(error => {
            loading.classList.add('hidden');
            showError("Une erreur s'est produite: " + error.message);
            console.error('Erreur:', error);
        });
    });
    
    function showError(message) {
        errorContainer.classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
    }
    
    function displayResults(data) {
        try {
            // Afficher le JSON brut pour debug
            document.getElementById('jsonResult').textContent = JSON.stringify(data, null, 2);
            
            // Remplir le dashboard avec les données
            if (data.raisonnement) {
                document.getElementById('reasoning').innerHTML = formatText(data.raisonnement);
            }
            
            if (data.produit_recommande) {
                document.getElementById('productName').textContent = data.produit_recommande;
            }
            
            if (data.branche) {
                document.getElementById('productBranch').textContent = data.branche;
                document.getElementById('branchName').textContent = data.branche;
                
                // Changer l'icône selon la branche
                const branchIcon = document.getElementById('branchIcon');
                branchIcon.innerHTML = getBranchIcon(data.branche);
                branchIcon.className = `w-16 h-16 rounded-full flex items-center justify-center mb-3 ${getBranchColor(data.branche)}`;
            }
            
            if (data.score_pertinence) {
                const score = parseInt(data.score_pertinence.toString().replace('/100', ''));
                document.getElementById('scoreText').textContent = `${score}/100`;
                renderScoreChart(score);
            }
            
            if (data.pitch) {
                document.getElementById('pitch').innerHTML = formatText(data.pitch);
            }
            
            if (data.conditions_generales) {
                document.getElementById('conditions').innerHTML = formatText(data.conditions_generales);
            }
        } catch (error) {
            console.error('Erreur lors de l\'affichage des résultats:', error);
            showError("Erreur lors de l'affichage des résultats");
        }
    }
    
    function formatText(text) {
        if (!text) return '';
        // Convertir les sauts de ligne en <br> et les listes en HTML
        return text.toString()
                   .replace(/\n/g, '<br>')
                   .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                   .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }
    
    function getBranchIcon(branche) {
        const icons = {
            "Assurance Vie": `<svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>`,
            "Assurance Santé": `<svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
            </svg>`,
            "Assurance Transport": `<svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M8 17a1 1 0 011-1h6a1 1 0 110 2H9a1 1 0 01-1-1z"></path>
                <path fill-rule="evenodd" d="M16 3a4 4 0 00-3.163 6.5H7.163A4 4 0 104 11.837v.663A2.5 2.5 0 006.5 15h11a2.5 2.5 0 002.5-2.5v-.663A4 4 0 0016 3z" clip-rule="evenodd"></path>
            </svg>`
        };
        
        return icons[branche] || `<svg class="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
        </svg>`;
    }
    
    function getBranchColor(branche) {
        const colors = {
            "Assurance Vie": "bg-green-100 text-green-600",
            "Assurance Santé": "bg-red-100 text-red-600",
            "Assurance Transport": "bg-blue-100 text-blue-600"
        };
        return colors[branche] || "bg-gray-100 text-gray-600";
    }
    
    function renderScoreChart(score) {
        const ctx = document.getElementById('scoreChart');
        if (!ctx) return;
        
        // Vérifier si le chart existe déjà
        if (window.scoreChart instanceof Chart) {
            window.scoreChart.destroy();
        }
        
        window.scoreChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 100 - score],
                    backgroundColor: [
                        getScoreColor(score),
                        '#e5e7eb'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '80%',
                rotation: -90,
                circumference: 180,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        enabled: false
                    }
                }
            }
        });
    }
    
    function getScoreColor(score) {
        if (score >= 80) return '#10b981'; // vert
        if (score >= 60) return '#f59e0b'; // orange
        return '#ef4444'; // rouge
    }
});