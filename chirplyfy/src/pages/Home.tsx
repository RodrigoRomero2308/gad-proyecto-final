import { useState } from "react";
import { Message, getMessages } from "../data/messages";
import {
  IonContent,
  IonFooter,
  IonHeader,
  IonPage,
  IonText,
  IonTitle,
  IonToolbar,
  useIonViewWillEnter,
} from "@ionic/react";
import "./Home.css";
import SongSearchForm from "../components/SongSearchForm";

const Home: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);

  useIonViewWillEnter(() => {
    const msgs = getMessages();
    setMessages(msgs);
  });

  const refresh = (e: CustomEvent) => {
    setTimeout(() => {
      e.detail.complete();
    }, 3000);
  };

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

        {/* <IonList>
          {messages.map(m => <MessageListItem key={m.id} message={m} />)}
        </IonList> */}
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
