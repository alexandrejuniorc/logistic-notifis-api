import { FastifyTypedInstance } from "@/@types/fastify-instace";
import { oauthToken } from "./authentication.controller";

export async function authenticationRoutes(app: FastifyTypedInstance) {
  app.post("/oauth2/token", oauthToken);
}

