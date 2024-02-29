import { IonButton, IonImg, IonItem, IonLabel, IonLoading } from "@ionic/react";
import { BirdSong, useBirdsServices } from "../services/bird_song";
import styles from "./BirdSongItem.module.css";
import { useEffect, useRef, useState } from "react";

const BirdSongItem = ({ birdSong }: { birdSong: BirdSong }) => {
  const { fetchBirdImages } = useBirdsServices();
  const [birdImageUrl, setBirdImageUrl] = useState<string>();
  const controllerRef = useRef<AbortController>();

  const fetchImage = async (signal: AbortSignal) => {
    try {
      const url = await fetchBirdImages(birdSong.common_name, signal);
      setBirdImageUrl(url);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    controllerRef.current = new AbortController();
    const signal = controllerRef.current.signal;
    fetchImage(signal);

    return () => {
      controllerRef.current?.abort();
    };
  }, []);

  return (
    <div
      key={birdSong.id}
      style={{
        minWidth: "100%",
      }}
    >
      <IonItem
        className={birdImageUrl ? styles["bird-song-item"] : ""}
        detail={false}
      >
        <div
          className={`ion-margin-vertical ${styles["bird-song-item-content"]}`}
          style={{
            minWidth: "100%",
          }}
        >
          <div
            key="background"
            style={{
              borderRadius: 6,
              overflow: "hidden",
            }}
          >
            <IonImg
              className={styles["bird-song-item-content-image"]}
              src={birdImageUrl}
            ></IonImg>
          </div>
          <div
            key="content"
            style={{
              zIndex: 1,
              background: "rgba(0, 0, 0, 0.5)",
              borderRadius: 4,
              minWidth: "100%",
            }}
            className="ion-padding"
          >
            <IonLabel
              className="ion-margin"
              style={{
                display: "block",
              }}
              color="dark"
            >
              <h2>Bird name: {birdSong.common_name}</h2>
              <h3>Bird scientific name: {birdSong.scientific_name}</h3>
              <h3>
                Distance with uploaded song:{" "}
                {birdSong.distancia_con_vector.toFixed(4)}
              </h3>
            </IonLabel>
            <div className="ion-margin">
              <audio
                style={{
                  minWidth: "100%",
                }}
                controls
                autoPlay={false}
              >
                <source src={birdSong.fileurl}></source>
              </audio>
            </div>
            {birdImageUrl ? (
              <IonButton
                href={`https://pixabay.com/images/search/?q=${birdSong.common_name}`}
                target="_blank"
                rel="noopener noreferrer"
                expand="block"
              >
                Get a closer look on Pixabay
              </IonButton>
            ) : null}
            <IonButton
              expand="block"
              href={`https://en.wikipedia.org/wiki/${encodeURI(
                birdSong.common_name
              )}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              Dive deeper on Wikipedia
            </IonButton>
          </div>
        </div>
      </IonItem>
    </div>
  );
};

export default BirdSongItem;
