export interface DatastoreValueModel {
    key: string;
    type: "text" | "number" | "boolean" | "list";
    default_value: string;
    temporary: boolean;
}