import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getDatabase } from "firebase/database";

const firebaseConfig = {
  apiKey: "AIzaSyAPFs37AVdFJO4qcIa0H3f-wxuJAq8DKR8",
  authDomain: "aidatos.firebaseapp.com",
  projectId: "aidatos",
  storageBucket: "aidatos.firebasestorage.app",
  messagingSenderId: "212234527915",
  appId: "1:212234527915:web:f575b0e22787f4bcae03ee",
  databaseURL: "https://aidatos.firebaseio.com"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);

export { auth, database };
