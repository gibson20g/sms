"""
Design System Tokens — Emerald & Cyan Messaging Interface
Refletindo 100% dos tokens do DESIGN.md e do protótipo Stitch
"""

class Colors:
    # Superfícies & Fundo
    BACKGROUND = "#FAF8FF"
    SURFACE = "#FAFAFA"
    SURFACE_CONTAINER = "#EAEDFF"
    SURFACE_CONTAINER_LOW = "#F2F3FF"
    SURFACE_CONTAINER_LOWEST = "#FFFFFF"
    SURFACE_CONTAINER_HIGH = "#E2E7FF"
    SURFACE_CONTAINER_HIGHEST = "#DAE2FD"
    
    # Texto & Bordas
    ON_SURFACE = "#131B2E"          # Slate 900
    ON_SURFACE_VARIANT = "#3E4947"  # Slate 600
    OUTLINE = "#E2E8F0"             # Hairline border 0.5px
    OUTLINE_VARIANT = "#BDC9C6"
    TEXT_SECONDARY = "#64748B"
    
    # Modo Pessoal (Esmeralda)
    PRIMARY = "#0F766E"             # Esmeralda
    PRIMARY_CONTAINER = "#0F766E"
    ON_PRIMARY = "#FFFFFF"
    ON_PRIMARY_CONTAINER = "#A3FAEF"
    PRIMARY_FIXED = "#9CF2E8"
    
    # Modo Comercial (Ciano Elétrico)
    SECONDARY = "#0284C7"           # Ciano Elétrico
    SECONDARY_CONTAINER = "#5BB8FE"
    ON_SECONDARY = "#FFFFFF"
    ON_SECONDARY_CONTAINER = "#00476E"
    SECONDARY_FIXED = "#CCE5FF"
    
    # Status, Destaques & Erro
    TERTIARY = "#F59E0B"            # Ambar / Destaque
    TERTIARY_CONTAINER = "#945D00"
    ERROR = "#BA1A1A"
    ERROR_CONTAINER = "#FFDAD6"
    
    # Bolhas de Mensagem
    BUBBLE_INBOUND = "#FFFFFF"
    BUBBLE_OUTBOUND_PERSONAL = "#0F766E"
    BUBBLE_OUTBOUND_BUSINESS = "#0284C7"
    READ_CHECK_CYAN = "#38BDF8"

class Radius:
    SM = 4
    MD = 8      # Squircle comercial
    LG = 16     # Message bubbles standard
    XL = 24
    FULL = 9999 # Pills e Avatares pessoais

class Typography:
    FONT_FAMILY = "Plus Jakarta Sans"
