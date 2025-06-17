/**Offres */
const targetDate = new Date("2025-10-30T00:00:00").getTime();

const day_number = document.querySelector(".promoChrono .days .number")
const hours_number = document.querySelector(".promoChrono .hours .number")
const minutes_number = document.querySelector(".promoChrono .minutes .number") 
const secondes_number = document.querySelector(".promoChrono .secondes .number") 

const interval = setInterval(() => {
    const now = new Date().getTime();
    const diff = targetDate - now;

    if (diff <= 0) {
    clearInterval(interval);
    chrono.textContent = "Time's up!";
    return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const secs = Math.floor((diff % (1000 * 60)) / 1000);
    day_number.textContent = `${days}`
    hours_number.textContent = `${hours}`
    minutes_number.textContent = `${mins}`
    secondes_number.textContent = `${secs}`
}, 1000);
/**Offres */

/*product_list */
document.addEventListener("DOMContentLoaded", () => {
    /* Set background color for color choices */
    document.querySelectorAll('.color_choices').forEach(span => {
        span.style.backgroundColor = span.dataset.bg_color;
    });

    /* Color Variation Radio Buttons */
    const radioBtns = document.querySelectorAll('.product_card__btn-radio');
    radioBtns.forEach(radioBtn => {
        radioBtn.addEventListener("click", () => {
            const productCard = radioBtn.closest('.product_card');
            const productImg = productCard.querySelector('.product_card__img > img');
            const productLink = productCard.querySelector('.image_card');
            const cardPrice = productCard.querySelector('.product_card__price');
            const proRadioBtns = productCard.querySelectorAll('.product_card__btn-radio');

            const sp = radioBtn.dataset.sale_price;
            const op = radioBtn.dataset.original_price;
            const url = radioBtn.dataset.variation_id;

            // Update cart link with new variation
            const cartBtn = productCard.querySelector(".product_card__btn.cart");
            cartBtn.dataset.variation_id = url;

            // Set image and link
            productImg.src = radioBtn.dataset.img;
            productLink.href = `/product/${url}/`;

            // Update price display
            if (sp === op) {
                cardPrice.textContent = `$${op}`;
            } else {
                cardPrice.innerHTML = `
                    <span class="original_price">$${op}</span>
                    <span class="sale_price">$${sp}</span>
                `;
            }

            // Update selection UI
            proRadioBtns.forEach(btn => btn.classList.remove("selected"));
            radioBtn.classList.add("selected");

            // Update cart button state
            toggleActiveCartButtons();
        });
    });

    /* Toggle "Add to Cart" and "Favorite" Buttons */
    document.querySelectorAll('.product_card__btn').forEach(btn => {
        btn.addEventListener("click", () => {
            btn.classList.toggle("active");

            const isFav = btn.classList.contains("fav");
            const isCart = btn.classList.contains("cart");

            if (isFav) {
                btn.dataset.tooltip = btn.classList.contains("active")
                    ? "remove from wishlist"
                    : "add to wishlist";
            }

            if (isCart) {
                btn.dataset.tooltip = btn.classList.contains("active")
                    ? "remove from cart"
                    : "add to cart";
            }
        });
    });

    /* Update Cart Buttons Based on Cart State */
    function toggleActiveCartButtons() {
        const container = document.querySelector('.most_popular_products');
        if (!container) return;

        const keys = container.dataset.keys || ""; // e.g., "1,3,7"
        const cartButtons = document.querySelectorAll(".product_card__btn.cart");

        cartButtons.forEach(cartBtn => {
            const variation_id = cartBtn.dataset.variation_id;

            if (keys.includes(variation_id)) {
                cartBtn.classList.add('active');
                cartBtn.href = `/cart/remove/${variation_id}/`;
                cartBtn.dataset.tooltip = "remove from cart";
            } else {
                cartBtn.classList.remove('active');
                cartBtn.href = `/cart/add/${variation_id}/`;
                cartBtn.dataset.tooltip = "add to cart";
            }
        });
    }

    // Run on initial load
    toggleActiveCartButtons();
});
/*product_list */



/*Slider List Links*/
let slider = document.querySelector('.slider');
let listLinks = document.querySelector('.list_links');
let prevBtn = document.querySelector(".links_products .slider button.previous");
let nextBtn = document.querySelector(".links_products .slider button.next");

// Initialize currentTranslate with existing transform
let currentTranslate = new DOMMatrixReadOnly(getComputedStyle(listLinks).transform).m41;

function update() {
    const sliderWidth = slider.clientWidth;
    const listWidth = listLinks.scrollWidth;
    const minTranslate = Math.min(0, sliderWidth - listWidth);
    
    // Update button states
    prevBtn.style.opacity = currentTranslate < 0 ? 1 : 0;
    nextBtn.style.opacity = currentTranslate > minTranslate ? 1 : 0;
    prevBtn.disabled = currentTranslate >= 0;
    nextBtn.disabled = currentTranslate <= minTranslate;
}

function moveSlider(direction) {
    const sliderWidth = slider.clientWidth;
    const listWidth = listLinks.scrollWidth;
    const minTranslate = Math.min(0, sliderWidth - listWidth);
    const step = 140; // Match your item width + margin

    currentTranslate += direction * step;
    currentTranslate = Math.max(minTranslate, Math.min(0, currentTranslate));
    
    listLinks.style.transform = `translateX(${currentTranslate}px)`;
    update();
}

// Event listeners
prevBtn.addEventListener('click', () => moveSlider(1));
nextBtn.addEventListener('click', () => moveSlider(-1));

// Handle window resize
window.addEventListener('resize', () => {
    const sliderWidth = slider.clientWidth;
    const listWidth = listLinks.scrollWidth;
    const minTranslate = Math.min(0, sliderWidth - listWidth);
    
    currentTranslate = Math.max(minTranslate, Math.min(0, currentTranslate));
    listLinks.style.transform = `translateX(${currentTranslate}px)`;
    update();
});

update();
/*Slider List Links*/


document.addEventListener("DOMContentLoaded", () => {
    toggleActiveCartButtons();
});