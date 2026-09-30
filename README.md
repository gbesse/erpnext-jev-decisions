# ERPNext Jev Decisions

Experimental community alpha v0.1.1 · MIT.

## Français

Une app ERPNext qui évalue les notes des nouveaux Leads dans un job Frappe et ajoute un commentaire de décision. Elle ne change ni le statut ni le responsable du Lead.

Installation :

```sh
bench get-app https://github.com/gbesse/erpnext-jev-decisions.git
bench --site YOUR_SITE install-app frappe_jev
```

Variables serveur : `TYPESAFE_API_KEY`. Garder les secrets hors du dépôt et de la configuration visible par les utilisateurs.

Créer idéalement un champ personnalisé `jev_request_text` de type Small Text sur Lead. Le hook `Lead.after_insert` lit ce champ, puis `description`, puis les notes existantes. Sans texte, aucun appel n’est effectué. La décision et son empreinte sont inscrites dans un commentaire.

Avant d’appeler Jev, le job vérifie si le Lead possède déjà un commentaire pour le même texte et la même version de politique. Des jobs simultanés peuvent encore créer des commentaires en double.

## English

An ERPNext app that evaluates new Lead notes in a Frappe background job and adds a decision comment. It does not change the Lead status or owner.

Setup:

```sh
bench get-app https://github.com/gbesse/erpnext-jev-decisions.git
bench --site YOUR_SITE install-app frappe_jev
```

Server variables: `TYPESAFE_API_KEY`. Keep secrets outside the repository and user-visible configuration.

Prefer creating a `jev_request_text` Small Text custom field on Lead. The `Lead.after_insert` hook reads it, then `description`, then existing notes. Without text, no request is made. The decision and its fingerprint are written as a comment.

Before calling Jev, the job checks whether the Lead already has a comment for the same text and policy version. Concurrent jobs can still create duplicate comments.

## Español

Una aplicación ERPNext que evalúa las notas de nuevos Leads en una tarea de Frappe y añade un comentario de decisión. No cambia el estado ni el responsable del Lead.

Instalación:

```sh
bench get-app https://github.com/gbesse/erpnext-jev-decisions.git
bench --site YOUR_SITE install-app frappe_jev
```

Variables del servidor: `TYPESAFE_API_KEY`. Mantén los secretos fuera del repositorio y de la configuración visible para usuarios.

Se recomienda crear un campo personalizado `jev_request_text` de tipo Small Text en Lead. El hook `Lead.after_insert` lo lee y luego lee `description` y las notas existentes. Sin texto, no se hace ninguna solicitud. La decisión y su huella se guardan en un comentario.

Antes de llamar a Jev, el trabajo comprueba si el Lead ya tiene un comentario para el mismo texto y versión de política. Los trabajos simultáneos aún pueden crear comentarios duplicados.

## Verification / Vérification / Verificación

```sh
python3 -m unittest discover -s tests -v
```

Tests use synthetic Jev responses and host event fixtures. Threshold `0.9` in `policy.json` is an example and must be calibrated on labeled data before automatic actions. No live host or Jev service has been exercised. / Les tests utilisent des réponses synthétiques et le seuil doit être calibré ; aucun hôte ni service Jev réel n’a été testé. / Las pruebas usan respuestas sintéticas y el umbral debe calibrarse; no se ha probado un host ni un servicio Jev real.

Host reference / Référence de l’hôte / Referencia del host: https://docs.frappe.io/framework/user/en/python-api/hooks
