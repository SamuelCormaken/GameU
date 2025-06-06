// SIDEBAR
console.log("script.js loaded!");
const menuItems = document.querySelectorAll('.menu-item');
console.log(menuItems); // Debugging: Check if menuItems are being selected correctly
const postTypeInput = document.getElementById('post-type');
const switchBtn = document.getElementById('switchTypeBtn');
const imageForm = document.getElementById('image-form');
const tournamentForm = document.getElementById('tournament-form');
// THEME
const theme = document.querySelector('#theme');
const themeModal = document.querySelector('.customize-theme');
const fontSizes = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const colorPalette = document.querySelectorAll('.choose-color span');
const Bg1 = document.querySelector('.bg-1');
const Bg2 = document.querySelector('.bg-2');
const Bg3 = document.querySelector('.bg-3');

// REMOVE
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active');
        if (item.id != 'notifications') {
            document.querySelector('.notifications-popup').style.display = 'none';
        } else {
            document.querySelector('.notifications-popup').style.display = 'block';
            document.querySelector('#notifications .notification-count').style.display = 'none';
        }
    })
})

// THEME/DISPLAY CUSTOMIZATION
const openThemeModal = () => {
    themeModal.style.display = 'grid';
}
// Close model
const closeThemeModal = (e) => {
    if (e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

themeModal.addEventListener('click', closeThemeModal);
theme.addEventListener('click', openThemeModal);

// FONT
const removeSizeSelector = () => {
    fontSizes.forEach(size => {
        size.classList.remove('active');
    })
}
fontSizes.forEach(size => {
    size.addEventListener('click', () => {
        removeSizeSelector();
        let fontSize;
        size.classList.toggle('active');
        
        if (size.classList.contains('font-size-1')) {
            fontSize = '10px';
            root.style.setProperty('---sticky-top-left', '5.4rem');
            root.style.setProperty('---sticky-top-right', '5.4rem');
        } else if (size.classList.contains('font-size-2')) {
            fontSize = '13px';
            root.style.setProperty('---sticky-top-left', '5.4rem');
            root.style.setProperty('---sticky-top-right', '-7rem');
        }
        else if (size.classList.contains('font-size-3')) {
            fontSize = '16px';
            root.style.setProperty('---sticky-top-left', '-2rem');
            root.style.setProperty('---sticky-top-right', '-17rem');
        }
        else if (size.classList.contains('font-size-4')) {
            fontSize = '19px';
            root.style.setProperty('---sticky-top-left', '-5rem');
            root.style.setProperty('---sticky-top-right', '-25rem');
        }
        else if (size.classList.contains('font-size-5')) {
            fontSize = '22px';
            root.style.setProperty('---sticky-top-left', '-12rem');
            root.style.setProperty('---sticky-top-right', '-35rem');
        }
        // CHANGE FONT SIZE 
        document.querySelector('html').style.fontSize = fontSize;
    })
})

// Color Active Selector
const changeActiveColorClass = () => {
    colorPalette.forEach(colorPicker => {
        colorPicker.classList.remove('acitve');
    })
}

colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        let primary;
        changeActiveColorClass();
        if (color.classList.contains('color-1')) {
            primaryHue = 252;
        }
        else if (color.classList.contains('color-2')) {
            primaryHue = 52;
        }
        else if (color.classList.contains('color-3')) {
            primaryHue = 352;
        }
        else if (color.classList.contains('color-4')) {
            primaryHue = 152;
        }
        else if (color.classList.contains('color-5')) {
            primaryHue = 202;
        }
        color.classList.add('active');
        root.style.setProperty('--primary-color-hue', primaryHue);
    })
})

let lightColorLightness;
let darkColorLightness;
let whiteColorLightness;

const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);
}

Bg1.addEventListener('click', () => {
    Bg1.classList.add('active');
    Bg2.classList.remove('active');
    Bg3.classList.remove('active');
    window.location.reload();
})

Bg2.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '20%';
    lightColorLightness = '15%';

    Bg2.classList.add('active');
    Bg1.classList.remove('active');
    Bg3.classList.remove('active');
    changeBG();
})

Bg3.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '10%';
    lightColorLightness = '0%';

    Bg3.classList.add('active');
    Bg1.classList.remove('active');
    Bg2.classList.remove('active');
    changeBG();
})

// switchType function
let currentType = 'image';  // Track current form type

// switchType function to toggle between forms

switchBtn.addEventListener('click', function () {
    if (postTypeInput.value === 'image') {
      postTypeInput.value = 'tournament';
      imageForm.style.display = 'none';
      tournamentForm.style.display = 'block';
      switchBtn.textContent = 'Switch to Image Post';
    } else {
      postTypeInput.value = 'image';
      imageForm.style.display = 'block';
      tournamentForm.style.display = 'none';
      switchBtn.textContent = 'Switch to Tournament Post';
    }
  });