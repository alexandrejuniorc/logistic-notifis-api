import type { FastifyReply, FastifyRequest } from "fastify";

export async function health(request: FastifyRequest, reply: FastifyReply) {
  try {
    return reply.status(200).send({
      message: "Service is healthy",
      status: 200,
    });
  } catch (error) {
    console.error("An error ocurred:", error);
    return reply.status(500).send(error);
  }
}

