import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
    en: {
        translation: {
            "search_placeholder": "What are you looking for?",
            "search_button": "Search",
            "attractions_button": "Add attractions",
            "dark_mode_button": "Dark mode",
            "light_mode_button": "Light mode",
        },
    },
    ru: {
        translation: {
            "search_placeholder": "Что найти?",
            "search_button": "Поиск",
            "attractions_button": "Добавить достопримечательности",
            "dark_mode_button": "Темный режим",
            "light_mode_button": "Светлый режим",
        },
    },
};

i18n.use(initReactI18next).init({
    resources,
    lng: "ru", // По умолчанию русский язык
    interpolation: {
        escapeValue: false,
    },
});

export default i18n;