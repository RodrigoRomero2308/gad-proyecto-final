import { IonButton, IonIcon, IonLabel, IonList } from "@ionic/react";
import { BirdSong } from "../services/bird_song";
import BirdSongItem from "./BirdSongItem";
import { returnUpBackOutline } from "ionicons/icons";

const BirdSongsList = ({
  onDismiss,
  birdSongs,
}: {
  onDismiss: () => void;
  birdSongs: BirdSong[];
}) => {
  return (
    <>
      <IonButton onClick={onDismiss} className="ion-margin-bottom">
        <IonIcon slot="start" icon={returnUpBackOutline} />
        <IonLabel>Reset</IonLabel>
      </IonButton>
      <IonList>
        {birdSongs.map((item) => (
          <BirdSongItem birdSong={item} />
        ))}
      </IonList>
    </>
  );
};

export default BirdSongsList;