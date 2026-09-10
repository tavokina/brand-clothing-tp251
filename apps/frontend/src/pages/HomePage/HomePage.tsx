import { useTranslation } from "react-i18next";


export const HomePage = () => {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('home.hero_title')}</h1>
    </div>
  );
}