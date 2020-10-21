import http from "../axios";

class ApiService {
  getAllUsers() {
    return http.get("/test");
  }
}

export default new ApiService();
