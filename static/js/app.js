let nextButton = document.getElementById('next');
let prevButton = document.getElementById('prev');
let carousel = document.querySelector('.carousel');
let listHTML = document.querySelector('.carousel .list');
let seeMoreButtons = document.querySelectorAll('.seeMore');
let backButton = document.getElementById('back');

nextButton.onclick = function(){
    showSlider('next');
}
prevButton.onclick = function(){
    showSlider('prev');
}
let unAcceppClick;
const showSlider = (type) => {
    nextButton.style.pointerEvents = 'none';
    prevButton.style.pointerEvents = 'none';

    carousel.classList.remove('next', 'prev');
    let items = document.querySelectorAll('.carousel .list .item');
    if(type === 'next'){
        listHTML.appendChild(items[0]);
        carousel.classList.add('next');
    }else{
        listHTML.prepend(items[items.length - 1]);
        carousel.classList.add('prev');
    }
    clearTimeout(unAcceppClick);
    unAcceppClick = setTimeout(()=>{
        nextButton.style.pointerEvents = 'auto';
        prevButton.style.pointerEvents = 'auto';
    }, 2000)
}
seeMoreButtons.forEach((button) => {
    button.onclick = function(){
        carousel.classList.remove('next', 'prev');
        carousel.classList.add('showDetail');
    }
});
backButton.onclick = function(){
    carousel.classList.remove('showDetail');
}

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

/*Btns color choices*/
const radioBtns = document.querySelectorAll('.product_card__btn-radio')  
radioBtns.forEach( radioBtn => {
    radioBtn.addEventListener("click", () => {
        let productCard  = radioBtn.parentElement.parentElement,
            productImg   = productCard.querySelector('.product_card__img > img'),
            productLink  = productCard.querySelector('.image_card'),
            proRadioBtns = productCard.querySelectorAll('.product_card__btn-radio')
        
        const cardPrice     = productCard.querySelector('.product_card__price')
        const originalPrice = cardPrice.querySelector(".original_price");
        const salePrice     = cardPrice.querySelector(".sale_price");

        const sp = radioBtn.dataset.sale_price     /**sale price data */
        const op = radioBtn.dataset.original_price /**original price data */
        const url = radioBtn.dataset.variation_id

        productLink.href = ''
        productLink.href = `product/${url}/`

        if(sp === op){
            cardPrice.textContent = `$${op}`
        }else{
            cardPrice.innerHTML = `
                    <span class="original_price">$${op}</span>
                    <span class="sale_price">$${sp}</span>
            `
        }
        

        if (radioBtn.parentElement.parentElement === productCard){
            proRadioBtns.forEach(btn => btn.classList.remove("selected"))
            radioBtn.classList.add('selected')
            productImg.src = radioBtn.dataset.img
        }
        
        
    })

})

const spans = document.querySelectorAll('.color_choices')
spans.forEach(span=>{
    span.style.backgroundColor = span.dataset.bg_color
})

/*Btns color choices*/

const AddCartBtns = document.querySelectorAll('.product_card__btn');

AddCartBtns.forEach(btn => {
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

/*Footer*/
const dropdown_content = document.querySelectorAll("footer .col h1")
dropdown_content.forEach(el =>{
    const dropdown = el.parentElement.querySelector('.dropdown')
    el.addEventListener('click', ()=>{
        dropdown.classList.toggle("active")
    })
})
/*Footer*/

/* Product details */
const imgs = document.querySelectorAll(".product_details .option img");
imgs.forEach(img => {
    img.addEventListener('click', () => {
        document.querySelector('.slide').src = img.src;
        imgs.forEach(i => i.classList.remove('active'));
        img.classList.add('active');
    });
});
/* Product details */
