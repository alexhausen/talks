import { isValidCPF } from "./cpf";

// $ npm test

describe("CPF validation", () => {
  it("should validate a valid CPF", () => {
    expect(isValidCPF("729.192.590-83")).toBeTruthy();
    expect(isValidCPF("98579510074")).toBeTruthy();
  });

  // "unhappy" path
  it("should invalidate a CPF with digit mismatch", () => {
    expect(isValidCPF("98579510070")).toBeFalsy();
  });

  /*
  // branch 1T
  it("should invalidate a CPF of wrong length", () => {
    expect(isValidCPF("7806004408")).toBeFalsy();
    expect(isValidCPF("078060044087")).toBeFalsy();
  });
  */

  /*
  // critério: erros comuns de entrada (letra em campo numérico)
  it("should invalidate a CPF with unexpected chars", () => {
    expect(isValidCPF("a78060044087")).toBeFalsy();
  });
  */

  /*
  // regra de negócio
  it("should invalidate a CPF when all the digits are the same", () => {
    expect(isValidCPF("11111111111")).toBeFalsy();
  });
  */
});
