const productsTable = document.querySelector("#products-table");
const productForm = document.querySelector("#product-form");
const saleForm = document.querySelector("#sale-form");
const saleProduct = document.querySelector("#sale-product");
const lowStockFilter = document.querySelector("#low-stock-filter");
const refreshProducts = document.querySelector("#refresh-products");
const inventorySummary = document.querySelector("#inventory-summary");
const message = document.querySelector("#message");

const currency = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

let products = [];
let toastTimer;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function showMessage(text, type = "success") {
  window.clearTimeout(toastTimer);
  message.textContent = text;
  message.className = `toast show ${type}`;

  toastTimer = window.setTimeout(() => {
    message.className = "toast";
  }, 3800);
}

function formatApiError(error) {
  if (Array.isArray(error.detail)) {
    return error.detail
      .map((item) => `${item.loc?.join(".") || "campo"}: ${item.msg}`)
      .join(" | ");
  }

  return error.detail || "Nao foi possivel concluir a operacao.";
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(formatApiError(error));
  }

  return response.json();
}

function renderProducts() {
  if (products.length === 0) {
    productsTable.innerHTML = `
      <tr>
        <td colspan="4">Nenhum produto encontrado.</td>
      </tr>
    `;
    saleProduct.innerHTML = '<option value="">Nenhum produto disponivel</option>';
    inventorySummary.textContent = "Nenhum produto cadastrado.";
    return;
  }

  productsTable.innerHTML = products
    .map((product) => {
      const stockClass = product.quantidade <= 5 ? "stock-low" : "";
      const productName = escapeHtml(product.nome);

      return `
        <tr>
          <td>${product.id}</td>
          <td>${productName}</td>
          <td>${currency.format(Number(product.preco))}</td>
          <td class="${stockClass}">${product.quantidade}</td>
        </tr>
      `;
    })
    .join("");

  saleProduct.innerHTML = [
    '<option value="">Selecione um produto</option>',
    ...products.map(
      (product) =>
        `<option value="${product.id}">${escapeHtml(product.nome)} - estoque: ${product.quantidade}</option>`
    ),
  ].join("");

  const totalItems = products.reduce((sum, product) => sum + product.quantidade, 0);
  inventorySummary.textContent = `${products.length} produto(s), ${totalItems} unidade(s) em estoque.`;
}

async function loadProducts() {
  refreshProducts.disabled = true;
  productsTable.innerHTML = `
    <tr>
      <td colspan="4">Carregando...</td>
    </tr>
  `;

  try {
    const query = lowStockFilter.checked ? "?estoque_baixo=true" : "";
    products = await request(`/produtos${query}`);
    renderProducts();
  } catch (error) {
    productsTable.innerHTML = `
      <tr>
        <td colspan="4">Erro ao carregar produtos.</td>
      </tr>
    `;
    showMessage(error.message, "error");
  } finally {
    refreshProducts.disabled = false;
  }
}

productForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = new FormData(productForm);
  const payload = {
    nome: data.get("nome").trim(),
    preco: data.get("preco"),
    quantidade: Number(data.get("quantidade")),
  };

  try {
    await request("/produtos", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    productForm.reset();
    showMessage("Produto cadastrado com sucesso.");
    await loadProducts();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

saleForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const data = new FormData(saleForm);
  const payload = {
    itens: [
      {
        produto_id: Number(data.get("produto_id")),
        quantidade: Number(data.get("quantidade")),
      },
    ],
  };

  try {
    const sale = await request("/vendas", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    saleForm.reset();
    showMessage(`Venda registrada. Total: ${currency.format(Number(sale.valor_total))}`);
    await loadProducts();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

lowStockFilter.addEventListener("change", loadProducts);
refreshProducts.addEventListener("click", loadProducts);

loadProducts();
