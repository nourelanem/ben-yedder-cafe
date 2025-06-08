main.js
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');

    // Gestion du défilement pour la navigation
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        header.classList.toggle('scrolled', window.scrollY > 50);
    });

    if (document.getElementById('featured-list')) {
        loadFeaturedProducts();
    }

    if (document.getElementById('product-list')) {
        // Données statiques pour tester l'affichage
        const staticProducts = [
            {
                id: 1,
                name: "Café Colombien",
                description: "Riche et fruité",
                price: 10.99,
                image: null
            },
            {
                id: 2,
                name: "Café Éthiopien",
                description: "Notes florales",
                price: 12.99,
                image: null
            }
        ];
        displayProducts(staticProducts); // Test avec des données statiques
        // loadProducts(); // Commentez temporairement pour tester
        loadCategories();
    }

    if (document.getElementById('product-details')) {
        loadProductDetails();
        loadReviews();
    }

    if (document.getElementById('cart-items')) {
        loadCart();
    }

    if (document.getElementById('login-form')) {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
    }

    const categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.addEventListener('change', () => {
            const categoryId = categorySelect.value;
            loadProducts(categoryId);
        });
    }

    document.getElementById('sort-price-asc')?.addEventListener('click', () => {
        fetch('http://localhost:8000/api/products/')
            .then(response => response.json())
            .then(products => {
                products.sort((a, b) => a.price - b.price);
                displayProducts(products);
            });
    });

    document.getElementById('sort-price-desc')?.addEventListener('click', () => {
        fetch('http://localhost:8000/api/products/')
            .then(response => response.json())
            .then(products => {
                products.sort((a, b) => b.price - a.price);
                displayProducts(products);
            });
    });

    document.getElementById('review-form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!token) {
            alert('Vous devez être connecté pour poster un avis.');
            window.location.href = '/login/';
            return;
        }
        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;
        const productId = new URLSearchParams(window.location.search).get('id');

        if (!productId) {
            alert('Produit non spécifié.');
            return;
        }

        fetch('http://localhost:8000/api/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                product: parseInt(productId),
                rating: parseInt(rating),
                comment
            })
        })
        .then(response => {
            if (!response.ok) throw new Error('Erreur lors de l’envoi');
            return response.json();
        })
        .then(data => {
            alert('Avis envoyé avec succès !');
            document.getElementById('review-form').reset();
            loadReviews();
        })
        .catch(error => {
            alert('Erreur : ' + error.message);
        });
    });

    document.getElementById('checkout-button')?.addEventListener('click', () => {
        alert('Fonctionnalité de commande à implémenter par Membre 4.');
    });
});

function loadFeaturedProducts() {
    fetch('http://localhost:8000/api/products/')
        .then(response => response.json())
        .then(products => {
            const featured = products.slice(0, 5);
            displayProducts(featured, 'featured-list');
        })
        .catch(error => console.error('Erreur:', error));
}

function loadProducts(categoryId = '') {
    const url = categoryId
        ? `http://localhost:8000/api/products/?category=${categoryId}`
        : 'http://localhost:8000/api/products/';
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(products => {
            console.log('Réponse API:', products);
            displayProducts(products);
        })
        .catch(error => {
            console.error('Erreur détaillée:', error);
            alert(`Impossible de charger les produits. Détails: ${error.message}`);
        });
}

function displayProducts(products, containerId = 'product-list') {
    const productList = document.getElementById(containerId);
    productList.innerHTML = '';
    products.forEach((product, index) => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.style.opacity = '0';
        card.style.transition = 'opacity 0.5s, transform 0.5s';
        card.style.transform = 'translateY(20px)';
        card.innerHTML = `
            <img src="${product.image || '/static/images/191324406.jpg'}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.description}</p>
            <p>Prix: ${product.price}€</p>
            <button onclick="addToCart(${product.id})">Ajouter au panier</button>
            <a href="/product/?id=${product.id}" class="btn">Voir détails</a>
        `;
        productList.appendChild(card);
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

function loadCategories() {
    fetch('http://localhost:8000/api/categories/')
        .then(response => response.json())
        .then(categories => {
            const categorySelect = document.getElementById('category');
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur:', error));
}

function loadProductDetails() {
    const productId = new URLSearchParams(window.location.search).get('id');
    if (productId) {
        fetch(`http://localhost:8000/api/products/${productId}/`)
            .then(response => response.json())
            .then(product => {
                const details = document.getElementById('product-details');
                details.innerHTML = `
                    <h2>${product.name}</h2>
                    <img src="${product.image || '/static/images/191324406.jpg'}" alt="${product.name}">
                    <p>${product.description}</p>
                    <p>Prix: ${product.price}€</p>
                    <button onclick="addToCart(${product.id})">Ajouter au panier</button>
                `;
            })
            .catch(error => {
                console.error('Erreur:', error);
                alert('Impossible de charger les détails du produit.');
            });
    }
}

function loadReviews() {
    const productId = new URLSearchParams(window.location.search).get('id');
    if (productId) {
        fetch('http://localhost:8000/api/reviews/')
            .then(response => response.json())
            .then(reviews => {
                const reviewList = document.getElementById('review-list');
                reviewList.innerHTML = '';
                reviews
                    .filter(review => review.product === parseInt(productId))
                    .forEach(review => {
                        const div = document.createElement('div');
                        div.className = 'review';
                        div.innerHTML = `
                            <p><strong>${review.user}</strong> - ${review.rating}/5</p>
                            <p>${review.comment}</p>
                            <p><small>${new Date(review.created_at).toLocaleDateString()}</small></p>
                        `;
                        reviewList.appendChild(div);
                    });
            })
            .catch(error => console.error('Erreur:', error));
    }
}

function addToCart(productId) {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Vous devez être connecté pour ajouter au panier.');
        window.location.href = '/login/';
        return;
    }

    fetch('http://localhost:8000/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: 1
        })
    })
    .then(response => {
        if (!response.ok) throw new Error('Erreur lors de l’ajout au panier');
        return response.json();
    })
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        alert('Erreur : ' + error.message);
    });
}

function loadCart() {
    const token = localStorage.getItem('token');
    if (!token) {
        alert('Vous devez être connecté pour voir le panier.');
        window.location.href = '/login/';
        return;
    }

    fetch('http://localhost:8000/api/cart/add/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        const cartItems = document.getElementById('cart-items');
        const totalPrice = document.getElementById('total-price');
        cartItems.innerHTML = '';
        let total = 0;

        const items = data.items || [];
        items.forEach(item => {
            const div = document.createElement('div');
            div.className = 'cart-item';
            div.innerHTML = `
                <span>${item.product.name} x${item.quantity}</span>
                <span>${(item.price * item.quantity).toFixed(2)}€</span>
                <button onclick="removeFromCart(${item.id})">Supprimer</button>
            `;
            cartItems.appendChild(div);
            total += item.price * item.quantity;
        });

        totalPrice.textContent = total.toFixed(2);
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Impossible de charger le panier.');
    });
}

function removeFromCart(itemId) {
    alert('Fonctionnalité de suppression à implémenter par Membre 4.');
}

function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('http://localhost:8000/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) throw new Error('Erreur de connexion');
        return response.json();
    })
    .then(data => {
        localStorage.setItem('token', data.token);
        alert('Connexion réussie !');
        window.location.href = '/';
    })
    .catch(error => {
        alert('Erreur : ' + error.message);
    });
}