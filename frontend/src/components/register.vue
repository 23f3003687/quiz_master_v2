<template>
  <div
    class="d-flex justify-content-center align-items-center vh-100"

  >
    <div
      class="card shadow-sm p-4 w-100"
      style="
        max-width: 400px;
        background-color: rgba(255, 255, 255, 0.8);
        border: none;
      "
    >
      <h3 class="text-center mb-4">Create an Account</h3>
      <form @submit.prevent="register">
        <div class="mb-3">
          <label for="full_name" class="form-label">Full Name</label>
          <input
            type="text"
            v-model="full_name"
            class="form-control"
            id="full_name"
            required
          />
        </div>
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
        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input
            type="date"
            v-model="dob"
            class="form-control"
            id="dob"
            required
          />
        </div>
        <div class="mb-3">
          <label for="qualification" class="form-label">Qualification</label>
          <input
            type="text"
            v-model="qualification"
            class="form-control"
            id="qualification"
            required
          />
        </div>
        <button type="submit" class="btn btn-success w-100">Register</button>
      </form>
      <p v-if="errorMessage" class="text-danger text-center mt-3">
        {{ errorMessage }}
      </p>
      <p class="text-center mt-3">
        <small>
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </small>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";


export default {
  name: "Register",

  setup() {
    const email = ref("");
    const password = ref("");
    const full_name = ref("");
    const dob = ref("");
    const qualification = ref("");
    const errorMessage = ref("");
    const router = useRouter();

    const register = async () => {
      try {
        await axios.post("http://localhost:5000/auth/register", {
          email: email.value,
          password: password.value,
          full_name: full_name.value,
          dob: dob.value,
          qualification: qualification.value,
        });
        router.push("/login");
      } catch (error) {
        errorMessage.value = "Registration failed. Please try again.";
      }
    };

    return {
      email,
      password,
      full_name,
      dob,
      qualification,
      errorMessage,
      register,
      
    };
  },
};
</script>

<style scoped>
/* Optional: custom tweaks */
</style>
