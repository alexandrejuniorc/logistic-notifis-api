import { FastifyTypedInstance } from "@/@types/fastify-instace";
import { health } from "./health.controller";

export async function healthRoutes(app: FastifyTypedInstance) {
  app.get("/health", health);
}

