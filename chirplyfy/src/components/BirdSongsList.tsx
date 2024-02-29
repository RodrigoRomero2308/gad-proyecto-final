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
      {birdSongs.length ? (
        <IonList
          style={{
            background: "transparent",
          }}
        >
          {birdSongs.map((item) => (
            <BirdSongItem key={item.id} birdSong={item} />
          ))}
        </IonList>
      ) : (
        <div>
          <IonLabel
            color="primary"
            className="ion-margin"
            style={{
              display: "block",
            }}
          >
            <h2>No feathered friends found nearby.</h2>
          </IonLabel>
          <IonLabel
            color="secondary"
            className="ion-margin"
            style={{
              display: "block",
            }}
          >
            <h3>Expand your search radius or come back later.</h3>
          </IonLabel>
        </div>
      )}
    </>
  );
};

export default BirdSongsList;
