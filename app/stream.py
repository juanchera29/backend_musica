import yt_dlp

def obtener_url_video(query: str) -> str:
    ydl_opts = {
        'quiet': True,
        'format': 'best[ext=mp4]/best',  # 🔹 Formato seguro para video
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'nocheckcertificate': True,
        'force_generic_extractor': True  # 🔹 Evita el bug SABR
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)

            if 'entries' in info:
                if not info['entries']:
                    raise ValueError("No se encontraron resultados.")
                video = info['entries'][0]
            else:
                video = info

            # Extraer URL directa
            if 'url' in video:
                return video['url']

            for fmt in video.get('formats', []):
                if fmt.get('url'):
                    return fmt['url']

            raise ValueError("No se encontró una URL válida.")

    except Exception as e:
        raise ValueError(f"Error al obtener URL: {str(e)}")
