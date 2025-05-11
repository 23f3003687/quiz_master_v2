<template>
  <div class="auth-form">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email:</label>
        <input type="email" v-model="email" id="email" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p>
      Don't have an account?
      <router-link to="/register">Register here</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

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
        localStorage.setItem("access_token", response.data.access_token); // Save JWT token in localStorage
        router.push("/dashboard"); // Redirect to dashboard after successful login
      } catch (error) {
        errorMessage.value = "Invalid credentials, please try again.";
      }
    };

    return { email, password, errorMessage, login };
  },
};
</script>

<style scoped>
/* Add your styles here */
.auth-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  margin-top: 10px;
}
</style>
