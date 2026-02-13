import type { FastifyReply, FastifyRequest } from "fastify";
import {
  ERROR_INVALID_CNPJ,
  ERROR_NO_NOTFIS,
  NOTFIS_CONSIGNADO,
  NOTFIS_STANDARD,
} from "./mocked-data";

export async function notfis(request: FastifyRequest, reply: FastifyReply) {
  try {
    const query = request.query as Record<string, string | undefined>;

    if (
      query.cnpjCarrier === "00000000000000" ||
      query.cnpjCarrier === "invalid"
    ) {
      return reply.status(403).send(ERROR_INVALID_CNPJ);
    }

    if (query.nfNumber === "000000000") {
      return reply.status(404).send(ERROR_NO_NOTFIS);
    }

    if (query.shippingNumber) {
      return reply.status(200).send(NOTFIS_STANDARD);
    }

    if (query.nfNumber && query.serieNumber && query.cnpjBranch) {
      if (query.cnpjBranch === "59105999006974") {
        return reply.status(200).send(NOTFIS_CONSIGNADO);
      }

      return reply.status(200).send(NOTFIS_STANDARD);
    }

    if (query.dataStart && query.dataEnd && query.timeStart && query.timeEnd) {
      return reply.status(200).send(NOTFIS_STANDARD);
    }

    return reply.status(400).send({
      error: "invalid_request",
      message: "Missing or invalid query parameters.",
    });
  } catch (error) {
    console.error("An error ocurred:", error);
    return reply.status(500).send(error);
  }
}

