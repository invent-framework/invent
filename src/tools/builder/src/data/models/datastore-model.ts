import type { DatastoreValueModel } from "./datastore-value-model";

export interface DatastoreModel {
    [key: string]: DatastoreValueModel;
}