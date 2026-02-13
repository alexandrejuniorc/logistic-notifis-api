import { FastifyTypedInstance } from "@/@types/fastify-instace";
import { notifis } from "./notifis.controller";
import { verifyJWT } from "@/http/middlewares/verify-jwt.middleware";

export async function notifisRoutes(app: FastifyTypedInstance) {
  app.addHook("onRequest", verifyJWT);

  app.get("/logistics/notifis", notifis);
}

