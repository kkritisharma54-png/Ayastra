import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAsE4xKi8rFFzGciRmzARasPxTCucAhqlc",
  authDomain: "ayastra-28e23.firebaseapp.com",
  projectId: "ayastra-28e23",
  storageBucket: "ayastra-28e23.firebasestorage.app",
  messagingSenderId: "263137315820",
  appId: "1:263137315820:web:e1bb30c712d502be0bcec9"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export const signInWithGoogle = async () => {
  const result = await signInWithPopup(auth, googleProvider);
  return result.user;
};

export const signInWithEmail = async (email: string, password: string) => {
  const result = await signInWithEmailAndPassword(auth, email, password);
  return result.user;
};

export const signUpWithEmail = async (email: string, password: string) => {
  const result = await createUserWithEmailAndPassword(auth, email, password);
  return result.user;
};

export const firebaseSignOut = async () => {
  await signOut(auth);
  localStorage.clear();
};