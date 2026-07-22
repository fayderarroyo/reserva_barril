import { useState, useEffect } from 'react';
import { collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy } from 'firebase/firestore';
import { db } from './firebase';
import emailjs from '@emailjs/browser';
import './index.css';

const USERS = [
  "Daniel Sierra",
  "Shirly Madiedo",
  "Fayder Arroyo",
  "Rina Marmolejo",
  "Maria Monica Rodriguez",
  "Lina Pertuz",
  "Kevin"
];

// Reemplaza estos valores con los de tu cuenta de EmailJS
const EMAILJS_SERVICE_ID = "service_kxjwro8";
const EMAILJS_TEMPLATE_ID = "template_bsca2ya";
const EMAILJS_PUBLIC_KEY = "tDS7fOJ4BtNDwOPwX";

emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });

function App() {
  const [user, setUser] = useState(localStorage.getItem('currentUser') || null);
  const [selectedUser, setSelectedUser] = useState(USERS[0]);
  const [password, setPassword] = useState('');
  const [date, setDate] = useState('');
  const [reservations, setReservations] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  // Escuchar cambios en Firestore en tiempo real
  useEffect(() => {
    const q = query(collection(db, "reservations"), orderBy("date", "asc"));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const resData = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setReservations(resData);
      setLoading(false);
    }, (err) => {
      console.error("Error obteniendo reservas:", err);
      // Si hay error de permisos (firestore no inicializado), no mostramos alerta invasiva
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (password === '1234' || password === 'pellejo') {
      setUser(selectedUser);
      localStorage.setItem('currentUser', selectedUser);
      setError('');
    } else {
      setError('Contraseña incorrecta');
    }
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('currentUser');
  };

  const notifyByEmail = (actionType, resDate) => {
    if (!EMAILJS_TEMPLATE_ID || EMAILJS_TEMPLATE_ID === "tu_template_id_aqui") return;

    const templateParams = {
      user_name: user,
      action: actionType === 'create' ? 'ha reservado el barril' : 'ha cancelado su reserva',
      date: resDate,
      to_email: "fayderarroyo@gmail.com, dmsierra10@gmail.com, shirlymadiedo@gmail.com, rinamarmolejo9@gmail.com, mamoca17@msn.com, lpertuz17@gmail.com, kevin9624@outlook.com"
    };

    emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams, { publicKey: EMAILJS_PUBLIC_KEY })
      .then((result) => {
        console.log('Email enviado con éxito:', result.text);
      })
      .catch((error) => {
        console.error('Error al enviar email:', error);
        alert(`Aviso EmailJS: No se pudo enviar el correo (${error?.text || error?.message || 'Error desconocido'}). Revisa tu Service ID o la plantilla.`);
      });
  };

  const handleReserve = async (e) => {
    e.preventDefault();
    if (!date) return;

    const hasActive = reservations.find(r => r.user === user);
    if (hasActive) {
      alert('Ya tienes una reserva activa. Cancélala primero.');
      return;
    }

    const dateTaken = reservations.find(r => r.date === date);
    if (dateTaken) {
      alert('Esta fecha ya está reservada por ' + dateTaken.user);
      return;
    }

    try {
      await addDoc(collection(db, "reservations"), {
        user,
        date,
        createdAt: new Date().toISOString()
      });
      setDate('');
      alert('¡Reserva confirmada con éxito en la nube! 🔥');
      notifyByEmail('create', date);
    } catch (err) {
      console.error(err);
      alert('Hubo un error al guardar. Asegúrate de configurar las reglas en Firestore.');
    }
  };

  const handleCancel = async (id, resDate) => {
    if(confirm('¿Seguro que deseas cancelar esta reserva?')) {
      try {
        await deleteDoc(doc(db, "reservations", id));
        notifyByEmail('cancel', resDate);
      } catch (err) {
        console.error(err);
        alert('Hubo un error al cancelar.');
      }
    }
  };

  if (!user) {
    return (
      <div className="auth-page">
        <div className="glass-panel auth-box">
          <h2 style={{ fontSize: '36px', marginBottom: '10px' }}>🔥 🥩 🍖</h2>
          <h1 style={{fontSize: '28px', background: 'linear-gradient(to right, #ea580c, #f59e0b)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>
            Reserva Barril
          </h1>
          <p style={{color: 'var(--text-secondary)', marginTop: '8px', fontSize: '18px'}}>"Los Rehabilitados"</p>
          <form className="auth-form" onSubmit={handleLogin}>
            <select 
              className="input-field" 
              value={selectedUser} 
              onChange={e => setSelectedUser(e.target.value)}
            >
              {USERS.map(u => <option key={u} value={u}>{u}</option>)}
            </select>
            <input 
              type="password" 
              className="input-field" 
              placeholder="Contraseña" 
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
            {error && <div style={{color: 'var(--danger-color)', fontSize: '14px', fontWeight: '500'}}>{error}</div>}
            <button type="submit" className="btn" style={{marginTop: '10px'}}>Ingresar al Sistema</button>
          </form>
        </div>
      </div>
    );
  }

  const myReservations = reservations.filter(r => r.user === user);
  const futureReservations = reservations.filter(r => new Date(r.date) >= new Date(new Date().setHours(0,0,0,0)));

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-container">
        <header className="header">
          <h1>🍖 Reserva Barril</h1>
          <div className="user-info">
            <span>👤 {user}</span>
            <button className="btn btn-danger" onClick={handleLogout}>Cerrar Sesión</button>
          </div>
        </header>

        <div className="grid">
          <div className="card">
            <div className="glass-panel">
              <h3 style={{fontSize: '22px'}}>📝 Hacer una Reserva</h3>
              <p style={{color: 'var(--text-secondary)', marginTop: '8px'}}>Selecciona el día de tu próximo asado.</p>
              <form onSubmit={handleReserve} style={{display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '24px'}}>
                <input 
                  type="date" 
                  className="input-field"
                  value={date}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={e => setDate(e.target.value)}
                  required
                />
                <button type="submit" className="btn" style={{width: '100%', fontSize: '18px', padding: '16px'}}>Confirmar Reserva 🔥</button>
              </form>
            </div>

            <div className="glass-panel">
              <h3 style={{fontSize: '22px'}}>🎫 Mis Reservas Activas</h3>
              <div style={{marginTop: '20px'}}>
                {loading ? (
                  <p style={{color: 'var(--text-secondary)'}}>Cargando de la nube...</p>
                ) : myReservations.length === 0 ? (
                  <p style={{color: 'var(--text-secondary)', fontStyle: 'italic'}}>No tienes reservas registradas.</p>
                ) : (
                  myReservations.map(r => (
                    <div key={r.id} className="reservation-item">
                      <span className="reservation-date">📅 {r.date}</span>
                      <button className="btn btn-danger" style={{padding: '8px 16px', fontSize: '14px'}} onClick={() => handleCancel(r.id, r.date)}>
                        Cancelar
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          <div className="card">
            <div className="glass-panel" style={{height: '100%'}}>
              <img src={`${import.meta.env.BASE_URL}grill_accent_light.jpg`} alt="Grill Accent" className="hero-image-small" />
              <h3 style={{fontSize: '22px'}}>📆 Calendario de Reservas</h3>
              <p style={{color: 'var(--text-secondary)', marginTop: '8px', marginBottom: '20px'}}>Próximos eventos en vivo.</p>
              <div>
                {loading ? (
                  <p style={{color: 'var(--text-secondary)', textAlign: 'center', marginTop: '40px'}}>Sincronizando con Firebase...</p>
                ) : futureReservations.length === 0 ? (
                  <p style={{color: 'var(--text-secondary)', fontStyle: 'italic', textAlign: 'center', marginTop: '40px'}}>El calendario está libre. ¡Sé el primero en reservar!</p>
                ) : (
                  futureReservations.map(r => (
                    <div key={r.id} className="reservation-item">
                      <div>
                        <div className="reservation-date">📅 {r.date}</div>
                        <div className="reservation-user">Reservado por <strong style={{color: '#1e293b'}}>{r.user}</strong></div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        <footer className="footer">
          <p>© 2026 Fayder Arroyo — Data & BI · Innovación Tecnológica</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
