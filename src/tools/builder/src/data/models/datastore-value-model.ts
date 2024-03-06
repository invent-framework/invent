export interface DatastoreValueModel {
    key: string;
    type: "text" | "number";
    default_value: string;
    temporary: boolean;
}