// API конфигурация
const API_BASE_URL = 'http://localhost:8000/api';

// Класс для работы с API
class API {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    // Общий метод для выполнения запросов
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // GET запрос
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    // POST запрос
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    // PUT запрос
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // DELETE запрос
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Создаем экземпляр API
const api = new API(API_BASE_URL);

// Методы для работы с типами материалов
const materialTypesAPI = {
    getAll: () => api.get('/material-types'),
    getById: (id) => api.get(`/material-types/${id}`),
    create: (data) => api.post('/material-types', data),
    update: (id, data) => api.put(`/material-types/${id}`, data),
    delete: (id) => api.delete(`/material-types/${id}`)
};

// Методы для работы с типами продукции
const productTypesAPI = {
    getAll: () => api.get('/product-types'),
    getById: (id) => api.get(`/product-types/${id}`),
    create: (data) => api.post('/product-types', data),
    update: (id, data) => api.put(`/product-types/${id}`, data),
    delete: (id) => api.delete(`/product-types/${id}`)
};

// Методы для работы с цехами
const workshopsAPI = {
    getAll: () => api.get('/workshops'),
    getById: (id) => api.get(`/workshops/${id}`),
    create: (data) => api.post('/workshops', data),
    update: (id, data) => api.put(`/workshops/${id}`, data),
    delete: (id) => api.delete(`/workshops/${id}`)
};

// Методы для работы с продукцией
const productsAPI = {
    getAll: () => api.get('/products'),
    getById: (id) => api.get(`/products/${id}`),
    create: (data) => api.post('/products', data),
    update: (id, data) => api.put(`/products/${id}`, data),
    delete: (id) => api.delete(`/products/${id}`)
};

// Методы для работы со связями продукции и цехов
const productWorkshopsAPI = {
    getAll: () => api.get('/product-workshops'),
    getById: (id) => api.get(`/product-workshops/${id}`),
    create: (data) => api.post('/product-workshops', data),
    update: (id, data) => api.put(`/product-workshops/${id}`, data),
    delete: (id) => api.delete(`/product-workshops/${id}`)
};

// Методы для работы с калькулятором сырья
const calculatorAPI = {
    calculateMaterial: (data) => api.post('/calculator/calculate-material', data),
    getWorkshopsForProduct: (productId) => api.get(`/calculator/workshops-for-product/${productId}`),
    getTotalProductionTime: (productId) => api.get(`/calculator/total-production-time/${productId}`)
};

// Утилиты для работы с API
const apiUtils = {
    // Показать уведомление об ошибке
    showError: (message) => {
        showToast(message, 'error');
    },

    // Показать уведомление об успехе
    showSuccess: (message) => {
        showToast(message, 'success');
    },

    // Обработка ошибок API
    handleError: (error, context = '') => {
        console.error(`API Error ${context}:`, error);
        const message = error.message || 'Произошла ошибка при выполнении запроса';
        apiUtils.showError(message);
    },

    // Проверка доступности API
    async checkHealth() {
        try {
            const response = await fetch('http://localhost:8000/health');
            return response.ok;
        } catch (error) {
            return false;
        }
    }
};