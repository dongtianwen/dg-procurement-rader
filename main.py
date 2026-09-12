import scraper
import processor
import writer


def main():
    notices = scraper.run()
    leads = processor.run(notices)
    writer.run(leads, total_count=len(notices))
    print("=== 完成 ===")


if __name__ == "__main__":
    main()
