import pytest
import uuid

@pytest.mark.asyncio
async def test_auth_and_profiles(client):
    # 1. Register User
    reg_data = {
        "email": "user1@example.com",
        "phone": "+5511999999999",
        "password": "secretpassword"
    }
    res = await client.post("/api/v1/auth/register", json=reg_data)
    assert res.status_code == 201
    user_res = res.json()
    assert user_res["email"] == "user1@example.com"
    user_id = user_res["id"]

    # 2. Login
    login_data = {
        "phone_or_email": "user1@example.com",
        "password": "secretpassword"
    }
    res = await client.post("/api/v1/auth/login", json=login_data)
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get /auth/me
    res = await client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["id"] == user_id

    # 4. List profiles (auto-created default personal profile)
    res = await client.get("/api/v1/profiles/", headers=headers)
    assert res.status_code == 200
    profiles = res.json()
    assert len(profiles) == 1
    assert profiles[0]["type"] == "pessoal"

    # 5. Create Commercial Profile
    prof_data = {
        "type": "comercial",
        "display_name": "Café & Bistrô",
        "bio": "O melhor café da cidade"
    }
    res = await client.post("/api/v1/profiles/", json=prof_data, headers=headers)
    assert res.status_code == 201
    comercial_profile = res.json()
    assert comercial_profile["type"] == "comercial"
    assert comercial_profile["display_name"] == "Café & Bistrô"

    # 6. List profiles again
    res = await client.get("/api/v1/profiles/", headers=headers)
    assert len(res.json()) == 2


@pytest.mark.asyncio
async def test_messaging_and_feed(client, db_session):
    # Register 2 users
    u1_reg = await client.post("/api/v1/auth/register", json={"email": "alice@sms.com", "password": "pass"})
    u2_reg = await client.post("/api/v1/auth/register", json={"email": "bob@sms.com", "password": "pass"})
    u1 = u1_reg.json()
    u2 = u2_reg.json()

    # Login U1
    u1_tok = (await client.post("/api/v1/auth/login", json={"phone_or_email": "alice@sms.com", "password": "pass"})).json()["access_token"]
    u1_headers = {"Authorization": f"Bearer {u1_tok}"}

    # Get U1 and U2 profiles
    u1_profiles = (await client.get("/api/v1/profiles/", headers=u1_headers)).json()
    u1_pessoal_id = u1_profiles[0]["id"]

    # Login U2
    u2_tok = (await client.post("/api/v1/auth/login", json={"phone_or_email": "bob@sms.com", "password": "pass"})).json()["access_token"]
    u2_headers = {"Authorization": f"Bearer {u2_tok}"}
    u2_profiles = (await client.get("/api/v1/profiles/", headers=u2_headers)).json()
    u2_pessoal_id = u2_profiles[0]["id"]

    # Create conversation between U1 and U2
    conv_data = {
        "kind": "direta",
        "context": "pessoal",
        "tag": "familia",
        "participant_profile_ids": [u2_pessoal_id]
    }
    res = await client.post("/api/v1/conversations/", json=conv_data, headers=u1_headers)
    assert res.status_code == 201
    conv = res.json()
    conv_id = conv["id"]

    # List conversations feed with context and tag filter
    res = await client.get("/api/v1/conversations/?context=pessoal&tag=familia", headers=u1_headers)
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Send message with metadata
    msg_data = {
        "conversation_id": conv_id,
        "content_type": "audio",
        "content_text": "Ouça este áudio",
        "metadata": {
            "duration": 42,
            "waveform": [0.1, 0.5, 0.8, 0.3]
        }
    }
    res = await client.post("/api/v1/messages/", json=msg_data, headers=u1_headers)
    assert res.status_code == 201
    msg = res.json()
    assert msg["metadata"]["duration"] == 42

    # Bob marks message as read
    res = await client.post(f"/api/v1/messages/{msg['id']}/read", headers=u2_headers)
    assert res.status_code == 200
    assert res.json()["status"] == "lido"


@pytest.mark.asyncio
async def test_statuses_and_views(client, db_session):
    # Register user
    u_reg = await client.post("/api/v1/auth/register", json={"email": "carol@sms.com", "password": "pass"})
    tok = (await client.post("/api/v1/auth/login", json={"phone_or_email": "carol@sms.com", "password": "pass"})).json()["access_token"]
    headers = {"Authorization": f"Bearer {tok}"}
    profiles = (await client.get("/api/v1/profiles/", headers=headers)).json()
    profile_id = profiles[0]["id"]

    # Create dummy attachment in DB directly
    from app.models import Attachment
    attachment = Attachment(
        uploaded_by_profile_id=uuid.UUID(profile_id),
        storage_url="https://storage.sms.app/story1.jpg",
        mime_type="image/jpeg"
    )
    db_session.add(attachment)
    await db_session.commit()
    await db_session.refresh(attachment)

    # Post Status
    status_data = {
        "attachment_id": str(attachment.id),
        "caption": "Meu primeiro story!",
        "visibility": "publico"
    }
    res = await client.post("/api/v1/statuses/", json=status_data, headers=headers)
    assert res.status_code == 201
    st = res.json()
    assert st["caption"] == "Meu primeiro story!"

    # List active statuses
    res = await client.get("/api/v1/statuses/", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Record unique view
    status_id = st["id"]
    res = await client.post(f"/api/v1/statuses/{status_id}/view", headers=headers)
    assert res.status_code == 200
    assert res.json()["status_id"] == status_id
