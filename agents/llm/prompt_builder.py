import json


class PromptBuilder:

    def build(
        self,
        context: dict,
    ) -> str:

        finding = context["finding"]

        prompt = f"""
Tu es un expert technique spécialisé dans la migration de modules Odoo.

OBJECTIF
Analyser un problème potentiel détecté lors de la migration d'un module
Odoo {context["source_version"]} vers Odoo {context["target_version"]}.

MODULE
{context["module"]}

FINDING
Type : {finding["type"]}
Sévérité : {finding["severity"]}
Message : {finding["message"]}

CONTEXTE PYTHON
{json.dumps(
    context["python"],
    indent=2,
    ensure_ascii=False,
)}

CONTEXTE XML
{json.dumps(
    context["xml"],
    indent=2,
    ensure_ascii=False,
)}

CONTEXTE DATABASE
{json.dumps(
    context.get("database", {}),
    indent=2,
    ensure_ascii=False,
)}

CONTEXTE DATA
{json.dumps(
    context.get("data", {}),
    indent=2,
    ensure_ascii=False,
)}

INSTRUCTIONS
Analyse uniquement le finding fourni et le contexte associé.

Détermine :
1. si une modification est probablement nécessaire ;
2. le niveau de risque de migration ;
3. la raison technique ;
4. la recommandation à appliquer ;
5. ton niveau de confiance.

Ne propose pas de modification automatique du code.

FORMAT DE SORTIE ATTENDU
Retourne une réponse structurée contenant :

decision
risk
reason
recommendation
confidence
"""

        return prompt.strip()
