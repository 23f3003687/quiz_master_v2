<template>
  <div
    class="d-flex justify-content-center align-items-center vh-100"
    
  >
    <div
      class="card shadow-sm p-4 w-100"
      style="
        max-width: 400px;
        background-color: rgba(177, 223, 241, 0.27);
        border: none;
      "
    >
      <!-- Logo and app name -->
      <div class="text-center mb-3">
        <img
          :src="logo"
          alt="QuizMaster Logo"
          style="height: 100px"
          class="mb-2"
        />
        <h4 class="text-center mb-4">Login to Your Account!</h4>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            type="email"
            v-model="email"
            class="form-control"
            id="email"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            v-model="password"
            class="form-control"
            id="password"
            required
          />
        </div>
        <button type="submit" class="btn btn-success w-100">Login</button>
      </form>

      <!-- Error and Link -->
      <p v-if="errorMessage" class="text-danger text-center mt-3">
        {{ errorMessage }}
      </p>
      <p class="text-center mt-3">
        <small>
          Don't have an account?
          <router-link to="/register">Register here</router-link>
        </small>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";
import logo from "@/assets/logo.png";

export default {
  name: "Login",
  setup() {
    const email = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const router = useRouter();

    const login = async () => {
      try {
        const response = await axios.post("http://localhost:5000/auth/login", {
          email: email.value,
          password: password.value,
        });

        const token = response.data.access_token;
        const role = response.data.role;

        localStorage.setItem("access_token", token);
        localStorage.setItem("role", role);

        if (role === "Admin") {
          router.push("/dashboard");
        } else if (role === "User") {
          router.push("/user/dashboard");
        } else {
          errorMessage.value = "Unknown user role!";
        }
      } catch (error) {
        errorMessage.value = "Invalid credentials, please try again.";
      }
    };

    return {
      email,
      password,
      errorMessage,
      login,
      logo,
     
    };
  },
};
</script>
