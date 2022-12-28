/**
 * Validate a CPF
 * @param cpf CPF digits with optional ponctuation
 * @returns true if CPF is valid
 */
function isValidCPF(cpf: string): boolean {
  cpf = cpf.replace(/\D/g, "");
  if (cpf.length !== 11) return false;
  const cpfDigits: number[] = cpf.split("").map((item) => +item);
  const rest = (count: number) =>
    ((cpfDigits
      .slice(0, count - 12)
      .reduce((soma, item, index) => soma + item * (count - index), 0) *
      10) %
      11) %
    10;
  return rest(10) === cpfDigits[9] && rest(11) === cpfDigits[10];
}

export { isValidCPF };
