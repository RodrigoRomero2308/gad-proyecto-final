import {
  IonContent,
  IonFooter,
  IonHeader,
  IonPage,
  IonText,
  IonTitle,
  IonToolbar,
} from "@ionic/react";
import "./Home.css";
import SongSearchForm from "../components/SongSearchForm";

const Home: React.FC = () => {
  return (
    <IonPage id="home-page">
      <IonHeader>
        <IonToolbar>
          <IonTitle>Chirplyfy</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent className="ion-padding">
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Chirplyfy</IonTitle>
          </IonToolbar>
        </IonHeader>

        <SongSearchForm />
      </IonContent>
      <IonFooter>
        <IonToolbar>
          <div className="ion-padding">
            <IonText class="ion-text-wrap">
              Made with love by Chirplyfy's team. All rights reserved
            </IonText>
          </div>
        </IonToolbar>
      </IonFooter>
    </IonPage>
  );
};

export default Home;
