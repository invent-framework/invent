import type { MediaFileModel } from "./media-file-model";

export interface MediaModel {
    [key: string]: MediaFileModel;
}