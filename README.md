# Eden Palace Cinéma
## Système de recommandation de films

À la demande du client, un cinéma situé dans le département français de la Creuse, ce projet consiste en la création d'un moteur de recommandations de films. L'objectif est de développer un site Internet à destination de potentiels clients du cinéma, intégrant un système de recommandation de films afin de les aider à découvrir de nouveaux longs-métrages adaptés à leurs préférences.

## Instructions d'utilisation

1. **Installation des dépendances**

   Assurez-vous d'avoir les dépendances nécessaires pour exécuter l'algorithme. Vous pouvez les installer en utilisant la commande suivante :

   ```
   pip install -r requirements.txt
   ```

2. **Clonage du référentiel**

   Clonez le référentiel du projet en utilisant la commande suivante :

   ```
   git clone https://github.com/votre_utilisateur/repo.git
   ```

3. **Configuration du projet**

   Assurez-vous d'avoir les fichiers nécessaires pour exécuter l'algorithme. Vous devrez placer les fichiers suivants dans le répertoire du projet :

   - `.streamlit` : Ce dossier contient la configuration pour l'application Streamlit.
   - `app.py` : Le fichier principal contenant le code de l'application Streamlit.
   - `client_logo.png` : Le logo du client à afficher dans la barre latérale de l'application.
   - `client_logo_white.png` : Une version blanche du logo du client à afficher dans l'onglet "Accueil" de l'application.
   - `df_movies_model.csv` : Le jeu de données prétraité pour le modèle de recommandation.
   - `df_actors_final.csv` : Le jeu de données contenant des informations sur les acteurs de films.
   - `packages.txt` : Une liste des packages Python utilisés dans le projet.
   - `requirements.txt` : Un fichier contenant les dépendances spécifiques et leurs versions pour le projet.

4. **Exécution de l'application**

   Exécutez l'application en utilisant la commande suivante :

   ```
   streamlit run app.py
   ```

   Cela lancera l'application sur votre serveur local, et vous pourrez y accéder en ouvrant votre navigateur et en visitant l'URL `http://localhost:8501`.

5. **Utilisation de l'application**

   L'application est divisée en deux onglets : "Accueil" et "Trouver des films".

   - **Accueil** : Cet onglet vous présente le service de recommandation de films et vous encourage à l'utiliser. Il affiche le logo du client et fournit une brève introduction sur le fonctionnement du système de recommandation.

   - **Trouver des films** : Cet onglet vous permet de rechercher des films et d'obtenir des recommandations personnalisées. Voici comment l'utiliser :

     - Sélectionnez un film de votre choix dans la liste déroulante.
     - Choisissez le nombre de films que vous souhaitez que le système vous recommande (3, 5 ou 10).
     - Cliquez sur le bouton "C'est parti !" pour lancer l'algorithme et découvrir les résultats.

     Une barre de progression indiquera l'avancement du processus de recommandation. Une fois terminé, vous pourrez consulter la fiche de chaque film   proposé.
