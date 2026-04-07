from src.search import embed_text, search_collection
from src.models import get_models
from src.collection import create_collection, list_collections, delete_collection,patch_collection, get_collection_details,get_me_infos
from src.documents import add_document_to_collection, get_documents_collection, get_document, delete_document, delete_chunk
from src.admin import get_roles, patch_role, create_role, create_user, get_users, create_token, get_tokens, get_routers, get_providers, update_user, delete_user, delete_role, delete_token, get_tokens_by_user
from src.rerank import rerank_results
from time import time

if __name__=="__main__":
    """Check get_users with role_id
    Checker providers et routers
    """

    routes = get_routers()
    assert len(routes) > 0, "Aucun routeur n'a été récupéré depuis l'API."
    id_role = create_role(name="Test",permissions=["admin","create_public_collection","read_metric","provide_models"])
    limits = []
    for route in routes:
        print(route)
        limits.append({"router": route.get("id"),"type":"tpm","value":10000})
    patch_role(role_id=id_role, limits=limits)

    try:
        assert len(get_roles()[-1]["limits"]) == len(routes), "Les limites du rôle n'ont pas été mises à jour correctement."
        expires_timestamp = int(time()) + 30*24*3600
        id_user = create_user(name="test", email="test.test@test.fr", password="test", role=id_role, expires=expires_timestamp)
        update_user(budget=10000, user_id=id_user)
        try:
            assert get_users(id_role)[-1]["budget"] == 10000, "Le budget de l'utilisateur n'a pas été mis à jour correctement."

            token,id_token = create_token(user_id=id_user, name="token_test", expires=expires_timestamp)
            try:
                assert get_tokens(token_id=id_token)["expires"] == expires_timestamp, "La date d'expiration du token n'a pas été définie correctement."

                collection_id = create_collection(
                    API_KEY=token,
                    name="Collection Test",
                    description="Description de la collection de test",
                    visibility="private"
                )
                patch_collection(
                    API_KEY=token,
                    collection_id=collection_id,
                    name="Collection Test",
                    description="Description patchée de la collection de test",
                    visibility="private"
                )

                assert get_collection_details(collection_id=collection_id, API_KEY=token)["description"] == "Description patchée de la collection de test", "La description de la collection n'a pas été mise à jour correctement."

                assert list_collections(API_KEY=token)[-1]["id"] == collection_id, "La collection créée n'est pas présente dans la liste des collections."

                status = add_document_to_collection(
                    API_KEY=token,
                    collection=collection_id,
                    file="data/martin.guitteny_304288a9-955d-4224-9d9f-3f8e7fcb2a05_finance_bon_feedback.pdf",
                    metadata={"author": "John Doe"},
                    output_format="markdown"
                )
                
                print("status : ",status)
                status = add_document_to_collection(
                    API_KEY=token,
                    collection=collection_id,
                    file="data/Les miserables.txt",
                    metadata={"author": "John Doe"},
                    output_format="markdown"
                )

                print("status : ",status)
                documents = get_documents_collection(collection=collection_id, limit=100, offset=0, API_KEY=token)
                print("documents : ", documents)
                document = get_document(document_id=documents[0]["id"], API_KEY=token)
                assert document["id"] == documents[0]["id"], "Le document récupéré n'est pas correct."
                assert len(documents) == 2, "Le nombre de documents dans la collection n'est pas correct."

                models = get_models(API_KEY=token)
                assert len(models) > 0, "Aucun modèle n'a été récupéré depuis l'API."

                embeding = embed_text("Bonjour, comment ça va ?", model="bge-m3", API_KEY=token)
                print(embeding)
                assert "embedding" in embeding[0], "L'embedding n'a pas été généré correctement."

                docs = search_collection(
                    API_KEY=token, collection=[collection_id], query="Quels sont les points d'amélioration de participer dans une organisation a but non lucratif?", score_threshold=0.70)
                assert len(docs) == 3, "On devrait trouver 3 documents avec un seuil de 0.70 pour la question sur les points d'amélioration de participer dans une organisation à but non lucratif."

                docs2 = search_collection(
                    API_KEY=token, collection=[collection_id], query="Quels sont les points d'amélioration de participer dans une organisation a but non lucratif?", score_threshold=0.0)
                assert len(docs2) == 5, "On devrait trouver 5 documents avec un seuil de 0.0 pour la question sur les points d'amélioration de participer dans une organisation à but non lucratif."

                chunks = [d["chunk"]["content"] for d in docs]
                rerank = rerank_results(API_KEY=token, query="Quels sont les points d'amélioration?", documents= chunks, model="bge-reranker-v2-m3", top_n=5)
                assert len(rerank["results"]) == 3, "Le nombre de documents rerankés n'est pas correct."

                id_chunk = documents[0]["chunks"][0]["id"]
                delete_chunk(API_KEY=token, document_id=documents[0]["id"], chunk_id=id_chunk)
                chunks_after_deletion = get_documents_collection(collection=collection_id, limit=100, offset=0, API_KEY=token)[0]["chunks"]
                assert len(chunks_after_deletion) == len(documents[0]["chunks"]) - 1, "Le chunk n'a pas été supprimé correctement."

                delete_document(document_id=documents[1]["id"])
                documents_after_deletion = get_documents_collection(collection=collection_id, limit=100, offset=0, API_KEY=token)
                assert len(documents_after_deletion) == len(documents) - 1, "Le document n'a pas été supprimé correctement."

                delete_collection(API_KEY=token, collection_id=collection_id)
                collections_after_deletion = list_collections(API_KEY=token)
                assert all(c["id"] != collection_id for c in collections_after_deletion), "La collection n'a pas été supprimée correctement."
            finally:
                delete_token(token_id=token)
                tokens_after_deletion = get_tokens_by_user(user_id=id_user)
                assert all(t["id"] != token for t in tokens_after_deletion), "Le token n'a pas été supprimé correctement."
        finally:
            delete_user(user_id=id_user)
            users_after_deletion = get_users(id_role)
            assert all(u["id"] != id_user for u in users_after_deletion), "L'utilisateur n'a pas été supprimé correctement."

    finally:
        delete_role(role_id=id_role)
        roles_after_deletion = get_roles()
        assert all(r["id"] != id_role for r in roles_after_deletion), "Le rôle n'a pas été supprimé correctement."
