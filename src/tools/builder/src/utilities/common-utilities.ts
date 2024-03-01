 /**
 * Common Utility functions.
 */
export class CommonUtilities {	
    private static id_chars: string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    public static getRandomId(prefix="invent", separator="_", length=10): string {
        let id: string = "";
        let count: number = 0;

        while (count < length){
            id += this.id_chars.charAt(Math.floor(Math.random() * this.id_chars.length));
            count += 1;
        }

        return `${prefix}${separator}${id}`
    }
}