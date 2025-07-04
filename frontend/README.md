# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

All backend routes follow REST principles. While not prefixed with /api/, they are structured cleanly and separately from frontend routing.

Answer for Not Using /api/ Prefix:

Yes, I actually used Flask Blueprints to organize my routes by module — for example, separate Blueprints for auth, admin, and user-related APIs.
Using Blueprints already gives structure and separation to the backend, so adding a /api/ prefix was optional in my case.
I kept routes clean and readable, like /auth/login and /admin/quiz, since my app is API-only and served via Vue.js.
However, I understand that in a production-grade system, adding an /api/ prefix helps separate frontend vs backend routes and supports versioning. I would absolutely adopt that if I were scaling the app or deploying it.”


Answer for Not Using Class-Based Views:
Since Blueprints already provided modular separation, I used function-based views (@route) for simplicity.
Class-based views like MethodView are more useful when I need to handle multiple HTTP methods on the same endpoint. For this project, since each route served a specific purpose and used one method (GET or POST), @route made things cleaner and easier to maintain.

Combining Blueprints and function-based routes helped me meet the milestones efficiently while keeping the codebase organized. If I had to expand the app further, I’d consider combining Blueprints with class-based views.

