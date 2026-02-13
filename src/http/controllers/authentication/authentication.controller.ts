import type { FastifyReply, FastifyRequest } from "fastify";
import { z } from "zod";
import { env } from "@/env";

const tokenBodySchema = z.object({
  grant_type: z.literal("client_credentials"),
  client_id: z.string().min(1),
  client_secret: z.string().min(1),
  scope: z.string().optional(),
});

function parseBasicAuth(header?: string) {
  if (!header || !header.startsWith("Basic ")) return null;
  const base64 = header.replace("Basic ", "");
  const decoded = Buffer.from(base64, "base64").toString("utf8");
  const [client_id, client_secret] = decoded.split(":");
  if (!client_id || !client_secret) return null;
  return { client_id, client_secret };
}

export async function oauthToken(request: FastifyRequest, reply: FastifyReply) {
  try {
    const basic = parseBasicAuth(request.headers.authorization);

    const requestBody =
      typeof request.body === "object" && request.body !== null
        ? (request.body as Record<string, unknown>)
        : {};

    const body = tokenBodySchema.parse({
      ...requestBody,
      client_id: basic?.client_id ?? (requestBody as any).client_id,
      client_secret: basic?.client_secret ?? (requestBody as any).client_secret,
    });

    const { client_id, client_secret } = body;

    if (
      client_id !== env.OAUTH_CLIENT_ID ||
      client_secret !== env.OAUTH_CLIENT_SECRET
    ) {
      return reply.status(401).send({
        error: "invalid_client",
        error_description: "Invalid client credentials.",
      });
    }

    const access_token = await reply.jwtSign(
      {
        scope: body.scope ?? "",
        client_id,
      },
      {
        sign: {
          sub: client_id,
          expiresIn: "24h",
        },
      },
    );

    return reply.status(200).send({
      access_token,
      token_type: "Bearer",
      expires_in: 86400,
      scope: body.scope ?? "",
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return reply.status(400).send({
        error: "invalid_request",
        error_description: "Invalid request payload.",
      });
    }

    console.error("An error ocurred:", error);
    return reply.status(500).send({
      error: "server_error",
      error_description: "Unexpected error.",
    });
  }
}

