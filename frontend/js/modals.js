// Функции для работы с модальными окнами

// Создание модального окна для типов материалов
function createMaterialTypeModal(materialType = null) {
    const isEdit = materialType !== null;
    const title = isEdit ? 'Редактировать тип материала' : 'Добавить тип материала';
    
    return `
        <div class="modal fade" id="materialTypeModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="materialTypeForm">
                            <div class="mb-3">
                                <label for="materialTypeName" class="form-label">Название *</label>
                                <input type="text" class="form-control" id="materialTypeName" 
                                       value="${isEdit ? materialType.name : ''}" required>
                            </div>
                            <div class="mb-3">
                                <label for="materialTypeLossPercentage" class="form-label">Процент потерь (%)</label>
                                <input type="number" class="form-control" id="materialTypeLossPercentage" 
                                       step="0.1" min="0" max="100"
                                       value="${isEdit ? (materialType.loss_percentage || '') : ''}">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="saveMaterialType(${isEdit ? materialType.id : null})">
                            ${isEdit ? 'Сохранить' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Создание модального окна для типов продукции
function createProductTypeModal(productType = null) {
    const isEdit = productType !== null;
    const title = isEdit ? 'Редактировать тип продукции' : 'Добавить тип продукции';
    
    return `
        <div class="modal fade" id="productTypeModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="productTypeForm">
                            <div class="mb-3">
                                <label for="productTypeName" class="form-label">Название *</label>
                                <input type="text" class="form-control" id="productTypeName" 
                                       value="${isEdit ? productType.name : ''}" required>
                            </div>
                            <div class="mb-3">
                                <label for="productTypeCoefficient" class="form-label">Коэффициент</label>
                                <input type="number" class="form-control" id="productTypeCoefficient" 
                                       step="0.1" min="0"
                                       value="${isEdit ? (productType.coefficient || '') : ''}">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="saveProductType(${isEdit ? productType.id : null})">
                            ${isEdit ? 'Сохранить' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Создание модального окна для цехов
function createWorkshopModal(workshop = null) {
    const isEdit = workshop !== null;
    const title = isEdit ? 'Редактировать цех' : 'Добавить цех';
    
    return `
        <div class="modal fade" id="workshopModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="workshopForm">
                            <div class="mb-3">
                                <label for="workshopName" class="form-label">Название *</label>
                                <input type="text" class="form-control" id="workshopName" 
                                       value="${isEdit ? workshop.name : ''}" required>
                            </div>
                            <div class="mb-3">
                                <label for="workshopType" class="form-label">Тип цеха</label>
                                <input type="text" class="form-control" id="workshopType" 
                                       value="${isEdit ? (workshop.workshop_type || '') : ''}">
                            </div>
                            <div class="mb-3">
                                <label for="workshopStaffCount" class="form-label">Количество персонала</label>
                                <input type="number" class="form-control" id="workshopStaffCount" 
                                       min="0"
                                       value="${isEdit ? (workshop.staff_count || '') : ''}">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="saveWorkshop(${isEdit ? workshop.id : null})">
                            ${isEdit ? 'Сохранить' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Создание модального окна для продукции
function createProductModal(product = null) {
    const isEdit = product !== null;
    const title = isEdit ? 'Редактировать продукцию' : 'Добавить продукцию';
    
    return `
        <div class="modal fade" id="productModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="productForm">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="productName" class="form-label">Название *</label>
                                        <input type="text" class="form-control" id="productName" 
                                               value="${isEdit ? product.name : ''}" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="productTypeId" class="form-label">Тип продукции</label>
                                        <select class="form-select" id="productTypeId">
                                            <option value="">Выберите тип продукции</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="productArticle" class="form-label">Артикул</label>
                                        <input type="text" class="form-control" id="productArticle" 
                                               value="${isEdit ? (product.article || '') : ''}">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="productMinPrice" class="form-label">Минимальная цена</label>
                                        <input type="number" class="form-control" id="productMinPrice" 
                                               step="0.01" min="0"
                                               value="${isEdit ? (product.min_price || '') : ''}">
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="productMainMaterial" class="form-label">Основной материал</label>
                                <input type="text" class="form-control" id="productMainMaterial" 
                                       value="${isEdit ? (product.main_material || '') : ''}">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="saveProduct(${isEdit ? product.id : null})">
                            ${isEdit ? 'Сохранить' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Создание модального окна для связей продукции и цехов
function createProductWorkshopModal(productWorkshop = null) {
    const isEdit = productWorkshop !== null;
    const title = isEdit ? 'Редактировать связь' : 'Добавить связь';
    
    return `
        <div class="modal fade" id="productWorkshopModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="productWorkshopForm">
                            <div class="mb-3">
                                <label for="productWorkshopProductId" class="form-label">Продукция *</label>
                                <select class="form-select" id="productWorkshopProductId" required>
                                    <option value="">Выберите продукцию</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="productWorkshopWorkshopId" class="form-label">Цех *</label>
                                <select class="form-select" id="productWorkshopWorkshopId" required>
                                    <option value="">Выберите цех</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="productWorkshopProductionTime" class="form-label">Время производства (часы)</label>
                                <input type="number" class="form-control" id="productWorkshopProductionTime" 
                                       step="0.1" min="0"
                                       value="${isEdit ? (productWorkshop.production_time_hours || '') : ''}">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                        <button type="button" class="btn btn-primary" onclick="saveProductWorkshop(${isEdit ? productWorkshop.id : null})">
                            ${isEdit ? 'Сохранить' : 'Добавить'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Функции для показа модальных окон
function showAddMaterialTypeModal() {
    showModal(createMaterialTypeModal());
}

function showEditMaterialTypeModal(materialType) {
    showModal(createMaterialTypeModal(materialType));
}

function showAddProductTypeModal() {
    showModal(createProductTypeModal());
}

function showEditProductTypeModal(productType) {
    showModal(createProductTypeModal(productType));
}

function showAddWorkshopModal() {
    showModal(createWorkshopModal());
}

function showEditWorkshopModal(workshop) {
    showModal(createWorkshopModal(workshop));
}

async function showAddProductModal() {
    showModal(createProductModal());
    await loadProductTypesForSelect();
}

async function showEditProductModal(product) {
    showModal(createProductModal(product));
    await loadProductTypesForSelect();
    if (product.product_type_id) {
        document.getElementById('productTypeId').value = product.product_type_id;
    }
}

async function showAddProductWorkshopModal() {
    showModal(createProductWorkshopModal());
    await loadProductsForSelect();
    await loadWorkshopsForSelect();
}

async function showEditProductWorkshopModal(productWorkshop) {
    showModal(createProductWorkshopModal(productWorkshop));
    await loadProductsForSelect();
    await loadWorkshopsForSelect();
    if (productWorkshop.product_id) {
        document.getElementById('productWorkshopProductId').value = productWorkshop.product_id;
    }
    if (productWorkshop.workshop_id) {
        document.getElementById('productWorkshopWorkshopId').value = productWorkshop.workshop_id;
    }
}

// Общая функция для показа модального окна
function showModal(modalHtml) {
    const container = document.getElementById('modal-container');
    container.innerHTML = modalHtml;
    const modal = new bootstrap.Modal(container.querySelector('.modal'));
    modal.show();
}

// Загрузка данных для селектов
async function loadProductTypesForSelect() {
    try {
        const productTypes = await productTypesAPI.getAll();
        const select = document.getElementById('productTypeId');
        select.innerHTML = '<option value="">Выберите тип продукции</option>';
        productTypes.forEach(type => {
            select.innerHTML += `<option value="${type.id}">${type.name}</option>`;
        });
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке типов продукции');
    }
}

async function loadProductsForSelect() {
    try {
        const products = await productsAPI.getAll();
        const select = document.getElementById('productWorkshopProductId');
        select.innerHTML = '<option value="">Выберите продукцию</option>';
        products.forEach(product => {
            select.innerHTML += `<option value="${product.id}">${product.name}</option>`;
        });
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке продукции');
    }
}

async function loadWorkshopsForSelect() {
    try {
        const workshops = await workshopsAPI.getAll();
        const select = document.getElementById('productWorkshopWorkshopId');
        select.innerHTML = '<option value="">Выберите цех</option>';
        workshops.forEach(workshop => {
            select.innerHTML += `<option value="${workshop.id}">${workshop.name}</option>`;
        });
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке цехов');
    }
}