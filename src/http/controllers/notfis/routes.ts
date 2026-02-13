import { FastifyTypedInstance } from "@/@types/fastify-instace";
import { notfis } from "./notfis.controller";
import { verifyJWT } from "@/http/middlewares/verify-jwt.middleware";

export async function notfisRoutes(app: FastifyTypedInstance) {
  app.addHook("onRequest", verifyJWT);

  app.get("/logistics/notfis", notfis);
}

