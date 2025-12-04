import streamlit as st

st.title("🔍 Test de Conexión Google Sheets")

# Test 1: Verificar si streamlit_gsheets está instalado
st.header("1. Verificar instalación")
try:
    from streamlit_gsheets import GSheetsConnection
    st.success("✅ streamlit_gsheets está instalado")
except ImportError as e:
    st.error(f"❌ streamlit_gsheets NO está instalado: {e}")

# Test 2: Intentar conectar
st.header("2. Intentar conexión")
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("✅ Conexión creada")
    
    # Test 3: Intentar leer
    st.header("3. Intentar leer datos")
    try:
        df = conn.read(worksheet="Reservas")
        st.success(f"✅ Datos leídos: {len(df)} filas")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Error al leer: {e}")
        
except Exception as e:
    st.error(f"❌ Error de conexión: {e}")

# Test 4: Mostrar secrets
st.header("4. Verificar secrets")
try:
    if "connections" in st.secrets:
        st.success("✅ Secrets configurados")
        st.write(st.secrets["connections"])
    else:
        st.error("❌ No hay secrets de conexión")
except Exception as e:
    st.error(f"❌ Error al leer secrets: {e}")
