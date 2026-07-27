import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

export const listResources = (page = 1, size = 9) =>
  api.get("/resources", { params: { page, size } }).then((res) => res.data);

export const createResource = (payload) =>
  api.post("/resources", payload).then((res) => res.data);

export const updateResource = (id, payload) =>
  api.put(`/resources/${id}`, payload).then((res) => res.data);

export const deleteResource = (id) =>
  api.delete(`/resources/${id}`);

export const smartAssist = (title, type) =>
  api.post("/resources/smart-assist", { title, type }).then((res) => res.data);

export default api;