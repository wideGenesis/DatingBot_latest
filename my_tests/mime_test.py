import mimetypes

mt = mimetypes.guess_type("https://ivapersonalblob.blob.core.windows.net/media/tg_1887695430/tmplugk49b6.mp4")
if mt:
    print("Mime Type:", mt[0])
else:
    print("Cannot determine Mime Type")

# Mime Type: application/pdf