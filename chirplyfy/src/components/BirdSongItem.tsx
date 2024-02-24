import { IonItem, IonLabel } from "@ionic/react";
import { BirdSong } from "../services/bird_song";

const BirdSongItem = ({ birdSong }: { birdSong: BirdSong }) => {
  return (
    <IonItem key={birdSong.id} detail={false}>
      <div>
        <IonLabel
          style={{
            display: "block",
          }}
        >
          <h2>Bird name: {birdSong.common_name}</h2>
          <p>Bird scientific name: {birdSong.scientific_name}</p>
          <p>
            Distance with uploaded song:{" "}
            {birdSong.distancia_con_vector.toFixed(4)}
          </p>
        </IonLabel>
        <div>
          <audio controls autoPlay={false}>
            <source src={birdSong.fileurl}></source>
          </audio>
        </div>
      </div>
    </IonItem>
  );
};

export default BirdSongItem;
