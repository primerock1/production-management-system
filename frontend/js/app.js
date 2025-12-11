// Глобальные переменные
let currentSection = 'dashboard';
let productTypesCache = [];
let productsCache = [];
let workshopsCache = [];

// Инициализация приложения
document.addEventListener('DOMContentLoaded', async function() {
    // Проверяем доступность API
    const isApiAvailable = await apiUtils.checkHealth();
    if (!isApiAvailable) {
        showToast('API сервер недоступен. Убедитесь, что backend запущен на порту 8000.', 'error');
        return;
    }

    // Загружаем панель управления
    await loadDashboard();
    
    // Устанавливаем активную навигацию
    updateNavigation('dashboard');
});

// Функция для показа секций
async function showSection(sectionName) {
    // Скрываем все секции
    document.querySelectorAll('.content-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Показываем выбранную секцию
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.classList.add('fade-in');
        currentSection = sectionName;
        
        // Обновляем навигацию
        updateNavigation(sectionName);
        
        // Загружаем данные для секции
        await loadSectionData(sectionName);
    }
}

// Обновление активной навигации
function updateNavigation(activeSection) {
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Находим и активируем соответствующую ссылку
    const activeLink = document.querySelector(`[onclick="showSection('${activeSection}')"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }
}

// Загрузка данных для секции
async function loadSectionData(sectionName) {
    try {
        switch (sectionName) {
            case 'dashboard':
                await loadDashboard();
                break;
            case 'material-types':
                await loadMaterialTypes();
                break;
            case 'product-types':
                await loadProductTypes();
                break;
            case 'workshops':
                await loadWorkshops();
                break;
            case 'products':
                await loadProducts();
                break;
            case 'product-workshops':
                await loadProductWorkshops();
                break;
            case 'calculator':
                showCalculatorSection();
                break;
        }
    } catch (error) {
        apiUtils.handleError(error, `при загрузке данных для ${sectionName}`);
    }
}

// Загрузка панели управления
async function loadDashboard() {
    try {
        const [materialTypes, productTypes, workshops, products] = await Promise.all([
            materialTypesAPI.getAll(),
            productTypesAPI.getAll(),
            workshopsAPI.getAll(),
            productsAPI.getAll()
        ]);

        document.getElementById('material-types-count').textContent = materialTypes.length;
        document.getElementById('product-types-count').textContent = productTypes.length;
        document.getElementById('workshops-count').textContent = workshops.length;
        document.getElementById('products-count').textContent = products.length;
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке статистики');
    }
}

// Загрузка типов материалов
async function loadMaterialTypes() {
    const tbody = document.querySelector('#material-types-table tbody');
    
    // Показываем индикатор загрузки
    tbody.innerHTML = `
        <tr>
            <td colspan="4" class="text-center py-4">
                <div class="loading-spinner me-2"></div>
                Загрузка данных...
            </td>
        </tr>
    `;
    
    try {
        const materialTypes = await materialTypesAPI.getAll();
        
        if (materialTypes.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center py-4">
                        <i class="fas fa-inbox fa-2x text-muted mb-2"></i>
                        <p class="text-muted mb-0">Нет данных для отображения</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = materialTypes.map(item => `
            <tr class="slide-in">
                <td><span class="badge bg-light text-dark">${item.id}</span></td>
                <td><strong>${item.name}</strong></td>
                <td>
                    ${item.loss_percentage !== null 
                        ? `<span class="badge bg-warning">${item.loss_percentage}%</span>` 
                        : '<span class="text-muted">-</span>'
                    }
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editMaterialType(${item.id})" 
                                title="Редактировать">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteMaterialType(${item.id})"
                                title="Удалить">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке типов материалов');
    }
}

// Загрузка типов продукции
async function loadProductTypes() {
    try {
        const productTypes = await productTypesAPI.getAll();
        productTypesCache = productTypes;
        const tbody = document.querySelector('#product-types-table tbody');
        
        if (productTypes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">Нет данных</td></tr>';
            return;
        }
        
        tbody.innerHTML = productTypes.map(item => `
            <tr>
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.coefficient !== null ? item.coefficient : '-'}</td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editProductType(${item.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteProductType(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке типов продукции');
    }
}

// Загрузка цехов
async function loadWorkshops() {
    try {
        const workshops = await workshopsAPI.getAll();
        workshopsCache = workshops;
        const tbody = document.querySelector('#workshops-table tbody');
        
        if (workshops.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Нет данных</td></tr>';
            return;
        }
        
        tbody.innerHTML = workshops.map(item => `
            <tr>
                <td>${item.id}</td>
                <td>${item.name}</td>
                <td>${item.workshop_type || '-'}</td>
                <td>${item.staff_count !== null ? item.staff_count : '-'}</td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="editWorkshop(${item.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-danger" onclick="deleteWorkshop(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке цехов');
    }
}

// Загрузка продукции
async function loadProducts() {
    try {
        const [products, productTypes] = await Promise.all([
            productsAPI.getAll(),
            productTypesAPI.getAll()
        ]);
        
        productsCache = products;
        productTypesCache = productTypes;
        
        const tbody = document.querySelector('#products-table tbody');
        
        if (products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Нет данных</td></tr>';
            return;
        }
        
        tbody.innerHTML = products.map(item => {
            const productType = productTypes.find(pt => pt.id === item.product_type_id);
            return `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>${productType ? productType.name : '-'}</td>
                    <td>${item.article || '-'}</td>
                    <td>${item.min_price !== null ? item.min_price.toLocaleString() + ' ₽' : '-'}</td>
                    <td>${item.main_material || '-'}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editProduct(${item.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteProduct(${item.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке продукции');
    }
}

// Загрузка связей продукции и цехов
async function loadProductWorkshops() {
    try {
        const [productWorkshops, products, workshops] = await Promise.all([
            productWorkshopsAPI.getAll(),
            productsAPI.getAll(),
            workshopsAPI.getAll()
        ]);
        
        const tbody = document.querySelector('#product-workshops-table tbody');
        
        if (productWorkshops.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Нет данных</td></tr>';
            return;
        }
        
        tbody.innerHTML = productWorkshops.map(item => {
            const product = products.find(p => p.id === item.product_id);
            const workshop = workshops.find(w => w.id === item.workshop_id);
            return `
                <tr>
                    <td>${item.id}</td>
                    <td>${product ? product.name : 'Неизвестно'}</td>
                    <td>${workshop ? workshop.name : 'Неизвестно'}</td>
                    <td>${item.production_time_hours !== null ? item.production_time_hours + ' ч' : '-'}</td>
                    <td>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editProductWorkshop(${item.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteProductWorkshop(${item.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке связей');
    }
}

// Функции для сохранения данных
async function saveMaterialType(id = null) {
    try {
        const name = document.getElementById('materialTypeName').value.trim();
        const lossPercentage = document.getElementById('materialTypeLossPercentage').value;
        
        if (!name) {
            showToast('Название обязательно для заполнения', 'error');
            return;
        }
        
        const data = {
            name: name,
            loss_percentage: lossPercentage ? parseFloat(lossPercentage) : null
        };
        
        if (id) {
            await materialTypesAPI.update(id, data);
            showToast('Тип материала обновлен', 'success');
        } else {
            await materialTypesAPI.create(data);
            showToast('Тип материала создан', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('materialTypeModal')).hide();
        await loadMaterialTypes();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при сохранении типа материала');
    }
}

async function saveProductType(id = null) {
    try {
        const name = document.getElementById('productTypeName').value.trim();
        const coefficient = document.getElementById('productTypeCoefficient').value;
        
        if (!name) {
            showToast('Название обязательно для заполнения', 'error');
            return;
        }
        
        const data = {
            name: name,
            coefficient: coefficient ? parseFloat(coefficient) : null
        };
        
        if (id) {
            await productTypesAPI.update(id, data);
            showToast('Тип продукции обновлен', 'success');
        } else {
            await productTypesAPI.create(data);
            showToast('Тип продукции создан', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('productTypeModal')).hide();
        await loadProductTypes();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при сохранении типа продукции');
    }
}

async function saveWorkshop(id = null) {
    try {
        const name = document.getElementById('workshopName').value.trim();
        const workshopType = document.getElementById('workshopType').value.trim();
        const staffCount = document.getElementById('workshopStaffCount').value;
        
        if (!name) {
            showToast('Название обязательно для заполнения', 'error');
            return;
        }
        
        const data = {
            name: name,
            workshop_type: workshopType || null,
            staff_count: staffCount ? parseInt(staffCount) : null
        };
        
        if (id) {
            await workshopsAPI.update(id, data);
            showToast('Цех обновлен', 'success');
        } else {
            await workshopsAPI.create(data);
            showToast('Цех создан', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('workshopModal')).hide();
        await loadWorkshops();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при сохранении цеха');
    }
}

async function saveProduct(id = null) {
    try {
        const name = document.getElementById('productName').value.trim();
        const productTypeId = document.getElementById('productTypeId').value;
        const article = document.getElementById('productArticle').value.trim();
        const minPrice = document.getElementById('productMinPrice').value;
        const mainMaterial = document.getElementById('productMainMaterial').value.trim();
        
        if (!name) {
            showToast('Название обязательно для заполнения', 'error');
            return;
        }
        
        const data = {
            name: name,
            product_type_id: productTypeId ? parseInt(productTypeId) : null,
            article: article || null,
            min_price: minPrice ? parseFloat(minPrice) : null,
            main_material: mainMaterial || null
        };
        
        if (id) {
            await productsAPI.update(id, data);
            showToast('Продукция обновлена', 'success');
        } else {
            await productsAPI.create(data);
            showToast('Продукция создана', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('productModal')).hide();
        await loadProducts();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при сохранении продукции');
    }
}

async function saveProductWorkshop(id = null) {
    try {
        const productId = document.getElementById('productWorkshopProductId').value;
        const workshopId = document.getElementById('productWorkshopWorkshopId').value;
        const productionTime = document.getElementById('productWorkshopProductionTime').value;
        
        if (!productId || !workshopId) {
            showToast('Продукция и цех обязательны для заполнения', 'error');
            return;
        }
        
        const data = {
            product_id: parseInt(productId),
            workshop_id: parseInt(workshopId),
            production_time_hours: productionTime ? parseFloat(productionTime) : null
        };
        
        if (id) {
            await productWorkshopsAPI.update(id, data);
            showToast('Связь обновлена', 'success');
        } else {
            await productWorkshopsAPI.create(data);
            showToast('Связь создана', 'success');
        }
        
        bootstrap.Modal.getInstance(document.getElementById('productWorkshopModal')).hide();
        await loadProductWorkshops();
    } catch (error) {
        apiUtils.handleError(error, 'при сохранении связи');
    }
}

// Функции для редактирования
async function editMaterialType(id) {
    try {
        const materialType = await materialTypesAPI.getById(id);
        showEditMaterialTypeModal(materialType);
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке типа материала');
    }
}

async function editProductType(id) {
    try {
        const productType = await productTypesAPI.getById(id);
        showEditProductTypeModal(productType);
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке типа продукции');
    }
}

async function editWorkshop(id) {
    try {
        const workshop = await workshopsAPI.getById(id);
        showEditWorkshopModal(workshop);
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке цеха');
    }
}

async function editProduct(id) {
    try {
        const product = await productsAPI.getById(id);
        await showEditProductModal(product);
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке продукции');
    }
}

async function editProductWorkshop(id) {
    try {
        const productWorkshop = await productWorkshopsAPI.getById(id);
        await showEditProductWorkshopModal(productWorkshop);
    } catch (error) {
        apiUtils.handleError(error, 'при загрузке связи');
    }
}

// Функции для удаления
async function deleteMaterialType(id) {
    if (!confirm('Вы уверены, что хотите удалить этот тип материала?')) return;
    
    try {
        await materialTypesAPI.delete(id);
        showToast('Тип материала удален', 'success');
        await loadMaterialTypes();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при удалении типа материала');
    }
}

async function deleteProductType(id) {
    if (!confirm('Вы уверены, что хотите удалить этот тип продукции?')) return;
    
    try {
        await productTypesAPI.delete(id);
        showToast('Тип продукции удален', 'success');
        await loadProductTypes();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при удалении типа продукции');
    }
}

async function deleteWorkshop(id) {
    if (!confirm('Вы уверены, что хотите удалить этот цех?')) return;
    
    try {
        await workshopsAPI.delete(id);
        showToast('Цех удален', 'success');
        await loadWorkshops();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при удалении цеха');
    }
}

async function deleteProduct(id) {
    if (!confirm('Вы уверены, что хотите удалить эту продукцию?')) return;
    
    try {
        await productsAPI.delete(id);
        showToast('Продукция удалена', 'success');
        await loadProducts();
        await loadDashboard();
    } catch (error) {
        apiUtils.handleError(error, 'при удалении продукции');
    }
}

async function deleteProductWorkshop(id) {
    if (!confirm('Вы уверены, что хотите удалить эту связь?')) return;
    
    try {
        await productWorkshopsAPI.delete(id);
        showToast('Связь удалена', 'success');
        await loadProductWorkshops();
    } catch (error) {
        apiUtils.handleError(error, 'при удалении связи');
    }
}

// Функция для показа уведомлений
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toastId = 'toast-' + Date.now();
    
    const toastHtml = `
        <div class="toast toast-${type}" role="alert" id="${toastId}">
            <div class="toast-body d-flex align-items-center">
                <i class="fas ${getToastIcon(type)} me-2"></i>
                <span class="flex-grow-1">${message}</span>
                <button type="button" class="btn-close btn-close-sm ms-2" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
    toast.show();
    
    // Удаляем элемент после скрытия
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

// ===== КАЛЬКУЛЯТОР СЫРЬЯ =====

// Загрузка данных для калькулятора
async function loadCalculatorData() {
    try {
        // Загружаем типы продукции
        const productTypes = await productTypesAPI.getAll();
        const productTypeSelect = document.getElementById('calc-product-type');
        productTypeSelect.innerHTML = '<option value="">Выберите тип продукции</option>';
        productTypes.forEach(type => {
            productTypeSelect.innerHTML += `<option value="${type.id}">${type.name} (коэф. ${type.coefficient})</option>`;
        });

        // Загружаем типы материалов
        const materialTypes = await materialTypesAPI.getAll();
        const materialTypeSelect = document.getElementById('calc-material-type');
        materialTypeSelect.innerHTML = '<option value="">Выберите тип материала</option>';
        materialTypes.forEach(type => {
            materialTypeSelect.innerHTML += `<option value="${type.id}">${type.name} (потери ${type.loss_percentage}%)</option>`;
        });

        // Загружаем продукты
        const products = await productsAPI.getAll();
        const productSelect = document.getElementById('product-select');
        productSelect.innerHTML = '<option value="">Выберите продукт для просмотра цехов</option>';
        products.forEach(product => {
            productSelect.innerHTML += `<option value="${product.id}">${product.name} (${product.article})</option>`;
        });

    } catch (error) {
        console.error('Ошибка загрузки данных для калькулятора:', error);
        showToast('Ошибка загрузки данных для калькулятора', 'error');
    }
}

// Обработка формы расчета сырья
function initCalculatorForm() {
    const form = document.getElementById('material-calculator-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                product_type_id: parseInt(document.getElementById('calc-product-type').value),
                material_type_id: parseInt(document.getElementById('calc-material-type').value),
                quantity: parseInt(document.getElementById('calc-quantity').value),
                param1: parseFloat(document.getElementById('calc-param1').value),
                param2: parseFloat(document.getElementById('calc-param2').value)
            };

            try {
                const result = await calculatorAPI.calculateMaterial(formData);
                displayCalculationResult(result);
            } catch (error) {
                console.error('Ошибка расчета:', error);
                showToast('Ошибка при расчете сырья: ' + error.message, 'error');
            }
        });
    }

    // Обработка выбора продукта для просмотра цехов
    const productSelect = document.getElementById('product-select');
    if (productSelect) {
        productSelect.addEventListener('change', async (e) => {
            const productId = e.target.value;
            if (productId) {
                await loadWorkshopsForProduct(productId);
            } else {
                document.getElementById('workshops-for-product').innerHTML = `
                    <div class="text-center text-muted">
                        <i class="fas fa-industry fa-3x mb-3"></i>
                        <p>Выберите продукт для просмотра цехов производства</p>
                    </div>
                `;
            }
        });
    }
}

// Отображение результата расчета
function displayCalculationResult(result) {
    const resultDiv = document.getElementById('calculation-result');
    
    if (result.success) {
        resultDiv.innerHTML = `
            <div class="alert alert-success">
                <h4><i class="fas fa-check-circle me-2"></i>Расчет выполнен успешно</h4>
                <div class="row text-start">
                    <div class="col-md-6">
                        <strong>Исходные данные:</strong>
                        <ul class="list-unstyled mt-2">
                            <li>Количество: ${result.quantity} шт.</li>
                            <li>Параметр 1: ${result.param1}</li>
                            <li>Параметр 2: ${result.param2}</li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <strong>Результат:</strong>
                        <div class="mt-2">
                            <span class="badge bg-primary fs-6">
                                ${result.required_material} единиц сырья
                            </span>
                        </div>
                    </div>
                </div>
                <p class="mb-0 mt-3"><small>${result.message}</small></p>
            </div>
        `;
        showToast('Расчет выполнен успешно', 'success');
    } else {
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <h4><i class="fas fa-exclamation-triangle me-2"></i>Ошибка расчета</h4>
                <p class="mb-0">${result.message}</p>
            </div>
        `;
        showToast('Ошибка при расчете', 'error');
    }
}

// Загрузка цехов для продукта
async function loadWorkshopsForProduct(productId) {
    try {
        const [workshops, totalTime] = await Promise.all([
            calculatorAPI.getWorkshopsForProduct(productId),
            calculatorAPI.getTotalProductionTime(productId)
        ]);

        const container = document.getElementById('workshops-for-product');
        
        if (workshops.length === 0) {
            container.innerHTML = `
                <div class="alert alert-warning">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Для данного продукта не найдено цехов производства
                </div>
            `;
            return;
        }

        let html = `
            <div class="alert alert-info mb-3">
                <div class="row">
                    <div class="col-md-8">
                        <strong>Продукт:</strong> ${totalTime.product_name}
                    </div>
                    <div class="col-md-4 text-end">
                        <strong>Общее время:</strong> 
                        <span class="badge bg-primary">${totalTime.total_production_time_hours} часов</span>
                    </div>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Цех</th>
                            <th>Тип цеха</th>
                            <th>Персонал</th>
                            <th>Время производства</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        workshops.forEach(workshop => {
            html += `
                <tr>
                    <td><strong>${workshop.workshop_name}</strong></td>
                    <td><span class="badge bg-secondary">${workshop.workshop_type}</span></td>
                    <td>${workshop.staff_count} чел.</td>
                    <td>${workshop.production_time_hours} ч.</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        container.innerHTML = html;

    } catch (error) {
        console.error('Ошибка загрузки цехов:', error);
        document.getElementById('workshops-for-product').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Ошибка при загрузке цехов: ${error.message}
            </div>
        `;
    }
}

// Показать раздел калькулятора
function showCalculatorSection() {
    loadCalculatorData();
    initCalculatorForm();
}