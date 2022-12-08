import datetime, uuid

# timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def unique_media_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"


def profile_unique_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/profiles/{instance._meta.model_name}/{uuid.uuid4().hex[:6]}.{ext}"


def logo_media_upload(instance, filename):
    ext = filename.split('.').pop()
    return f"images/{instance._meta.model_name}/{instance.abn}.{ext}"
