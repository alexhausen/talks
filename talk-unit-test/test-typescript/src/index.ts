// npx ts-node ./src/index.ts 780.600.440-87

import { isValidCPF } from "./cpf";

if (process.argv.length !== 3) {
  console.log("Wrong number of arguments");
  process.exit(1);
}

const cpf = process.argv[2];
console.log(`O CPF ${cpf} é ${isValidCPF(cpf) ? "válido" : "inválido"}.`);
