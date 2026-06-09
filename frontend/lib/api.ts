const BASE_URL = "http://127.0.0.1:8000";

// Get token from localStorage
const getToken = () => localStorage.getItem("token");

// Auth
export const signup = async (name: string, email: string, password: string) => {
  const res = await fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  return res.json();
};

export const login = async (email: string, password: string) => {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  if (data.access_token) {
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("name", data.name);
  }
  return data;
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("name");
};

// Products
export const getProducts = async () => {
  const res = await fetch(`${BASE_URL}/products`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};

export const sellProduct = async (productId: number, quantity: number) => {
  const res = await fetch(`${BASE_URL}/products/${productId}/sell?quantity=${quantity}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};

export const updateStock = async (productId: number, quantity: number) => {
  const res = await fetch(`${BASE_URL}/products/${productId}/stock?quantity=${quantity}`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};

// Brass Prices
export const getBrassPrices = async () => {
  const res = await fetch(`${BASE_URL}/brass-prices`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};

export const fetchLiveBrassPrice = async () => {
  const res = await fetch(`${BASE_URL}/brass-prices/fetch-live`, {
    method: "POST",
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};

// Scrap
export const getScrapRecommendation = async () => {
  const res = await fetch(`${BASE_URL}/scrap/recommendation`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  return res.json();
};