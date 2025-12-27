import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function OAuthCallback() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { setTokenFromOAuth } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    const error = searchParams.get('error');

    if (error) {
      navigate('/login?error=' + encodeURIComponent(error));
      return;
    }

    if (token) {
      // Save the token and fetch user profile
      setTokenFromOAuth(token);
      navigate('/dashboard');
    } else {
      navigate('/login?error=No token received');
    }
  }, [searchParams, navigate, setTokenFromOAuth]);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: 'linear-gradient(135deg, #52b788 0%, #40916c 100%)',
      color: 'white',
      fontSize: '1.5em'
    }}>
      Completing sign in...
    </div>
  );
}

export default OAuthCallback;


